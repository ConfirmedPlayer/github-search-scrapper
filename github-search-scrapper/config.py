import os


db_credentials = {
    'host': 'localhost',
    'user': os.environ['db_login'],
    'password': os.environ['db_password'],
    'database': 'github-search'
}


github_login = os.environ['github_login']
github_password = os.environ['github_password']
