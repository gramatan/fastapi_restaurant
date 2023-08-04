import asyncio
import logging

from app.database.utils import create_tables, drop_tables

logging.basicConfig(level=logging.INFO)


async def main():
    await drop_tables()
    await create_tables()

if __name__ == '__main__':
    asyncio.run(main())
