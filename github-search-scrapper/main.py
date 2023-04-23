import asyncio

from config import db_credentials, github_login, github_password
from github_session import GithubSession


async def main():
    session = await GithubSession(login=github_login,
                                  password=github_password,
                                  db_credentials=db_credentials).async_init()
    try:
        while True:
            query = input('Введите запрос для поиска: ')
            until_datetime = input('Введите дату и время. Например 20.04.2023 18:00 : ')
            await session.parse(query, until_datetime)
    finally:
        await session.close()


if __name__ == '__main__':
    asyncio.run(main())
