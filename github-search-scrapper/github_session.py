import asyncio
from datetime import datetime

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from database import Database


class GithubSession(Database):
    GITHUB_BASE_URL = 'https://github.com'

    def __init__(
        self,
        login: str,
        password: str,
        db_credentials: dict[str, str]
    ) -> None:

        self.login = login
        self.password = password

        self.session = ClientSession()
        self.__authorized = False

        super().__init__(db_credentials)

    async def _authorize(self) -> None:
        if self.__authorized:
            return

        print('Попытка авторизации...')

        async with self.session.get(f'{self.GITHUB_BASE_URL}/login') as response:
            html = await response.text()

        soup = BeautifulSoup(html, 'lxml')
        csrf_token = soup.find('input', {'name': 'authenticity_token'}).get('value')

        payload = {'login': self.login,
                   'password': self.password,
                   'authenticity_token': csrf_token,
                   'commit': 'Sign in'}

        async with self.session.post(f'{self.GITHUB_BASE_URL}/session', data=payload) as response:
            if response.status == 200:
                print(f'Авторизация успешна. Код: {response.status}')
                self.__authorized = True

    async def parse(self, query: str, until_datetime: str) -> None:
        while not self.__authorized:
            await self._authorize()
            if not self.__authorized:
                print('Ошибка авторизации. Спим 30 секунд...')
                await asyncio.sleep(30)

        until_datetime = datetime.strptime(until_datetime, '%d.%m.%Y %H:%M')
        params = {'o': 'desc',
                  'p': 1,
                  'q': query,
                  's': 'indexed',
                  'type': 'Code'}
        while True:
            async with self.session.get(f'{self.GITHUB_BASE_URL}/search', params=params) as resp:
                if resp.status != 200:
                    print('Ошибка при парсинге. Статус ответа != 200. Спим 30 секунд...')
                    await asyncio.sleep(30)
                    continue
                else:
                    html = await resp.text()

            soup = BeautifulSoup(html, 'lxml')
            results = soup.find_all('div', {'class': 'hx_hit-code'})
            if not results:
                print(f'Парсинг окончен. Всего страниц: {params["p"]}\n')
                return
            else:
                for result in results:
                    relative_time = result.find('relative-time').attrs['datetime']
                    relative_time = datetime.strptime(relative_time, '%Y-%m-%dT%H:%M:%SZ')
                    if relative_time < until_datetime:
                        print(f'Парсинг окончен. Всего страниц: {params["p"]}\n')
                        return

                    row_numbers = result.find_all('td', {'class': 'blob-num'})
                    for row_number in row_numbers:
                        row_number.decompose()

                    repository_url = result.find('a', {'class': 'Link--secondary'}).text
                    repository_url = ''.join(repository_url.split())
                    repository_url = f'{self.GITHUB_BASE_URL}/{repository_url}'

                    code_snippet = result.find('table', {'class': 'highlight'}).text

                    snippet_url = result.find('div', {'class': 'f4'}).children
                    snippet_url = list(snippet_url)[1].attrs['href']
                    snippet_url = f'{self.GITHUB_BASE_URL}{snippet_url}'

                    await self.insert_new_data(
                        query,
                        repository_url,
                        snippet_url,
                        relative_time,
                        code_snippet)

            params['p'] += 1

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()
