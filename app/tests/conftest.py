import os

# local
# URL = "http://127.0.0.1:8000"
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ylab:no_secure_password@localhost/resto"

# docker
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ylab:no_secure_password@db-test/resto"
# URL = "http://web-test:8000"

# get from env
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
URL = os.getenv("URL")
