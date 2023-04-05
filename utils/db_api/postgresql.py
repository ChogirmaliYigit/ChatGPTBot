from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from datetime import datetime
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None]
        self.now = datetime.now()

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_chats(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Chats (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        title VARCHAR(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_messages(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Messages (
        id SERIAL PRIMARY KEY,
        message TEXT NOT NULL,
        chat_id BIGINT NOT NULL,
        type VARCHAR(50) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id, created) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, full_name, username, telegram_id, self.now, fetchrow=True)

    async def add_chat(self, user_id, title):
        sql = "INSERT INTO chats (user_id, title, created) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, user_id, title, self.now, fetchrow=True)

    async def add_message(self, message, chat_id, type):
        sql = 'INSERT INTO messages (message, chat_id, type, created) VALUES($1, $2, $3, $4) returning *'
        return await self.execute(sql, message, chat_id, type, self.now, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_user_chats(self, **kwargs):
        sql = 'SELECT * FROM Chats WHERE '
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)
    
    async def select_chat(self, **kwargs):
        sql = 'SELECT * FROM Chats WHERE '
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_chat_messages(self, **kwargs):
        sql = 'SELECT * FROM Messages WHERE '
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_chat_title(self, title, user_id, id):
        sql = 'UPDATE Chats SET title=$1 WHERE user_id=$2 AND id=$3'
        return await self.execute(sql, title, user_id, id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)
    
    async def delete_chat(self, **kwargs):
        sql ='DELETE FROM Chats WHERE '
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        await self.execute(sql, *parameters, execute=True)
    
    async def delete_messages(self, **kwargs):
        sql ='DELETE FROM Messages WHERE '
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
