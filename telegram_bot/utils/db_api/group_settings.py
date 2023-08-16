from utils.db_api.db_gino import db
from asyncpg import UniqueViolationError
from utils.db_api.schemas.groups_settings import Settings

async def add_chat_settings(chat_id: int, chat_name: str):
    try:
        chat = Settings(chat_id=chat_id, chat_name=chat_name)
        await chat.create()
    except UniqueViolationError:
        print('Пользователь не добавлен')

async def select_all_chats():
    chats = await chats.query.gino.all()
    return chats

async def count_chats():
    count = await db.func.count(Settings.chat_id).gino.scalar()
    return count

async def select_chat(chat_id: int):
    chat = await Settings.query.where(Settings.chat_id == chat_id).gino.first()
    return chat

async def update_delete_links(chat_id: int, status: str):
    chat = await select_chat(chat_id)
    await chat.update(delete_link=status).apply()

async def update_delete_links_for_admin(chat_id: int, status: str):
    chat = await select_chat(chat_id)
    await chat.update(delete_admins_link=status).apply()