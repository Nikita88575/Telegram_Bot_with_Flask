from utils.db_api.db_gino import db
from asyncpg import UniqueViolationError
from utils.db_api.schemas.chat_rules import Chat_rules

async def add_rules(chat_id: int, rules: str):
    try:
        chat_rules = Chat_rules(chat_id=chat_id, rules=rules)
        await chat_rules.create()
    except UniqueViolationError:
        print('Пользователь не добавлен')

async def delete_rule(chat_id: int):
    try:
        delete_chat_rule = Chat_rules(chat_id=chat_id)
        await delete_chat_rule.delete()
    except UniqueViolationError:
        print('Пользователь не добавлен')

async def select_all_chats():
    chats = await chats.query.gino.all()
    return chats

async def count_chats():
    count = await db.func.count(Chat_rules.chat_id).gino.scalar()
    return count

async def select_chat(chat_id):
    chat = await Chat_rules.query.where(Chat_rules.chat_id == chat_id).gino.first()
    return chat

async def update_rules(chat_id, new_rules):
    chat = await select_chat(chat_id)
    await chat.update(rules=new_rules).apply()