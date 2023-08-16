from utils.db_api.db_gino import db
from asyncpg import UniqueViolationError
from utils.db_api.schemas.user import User

async def add_user(user_id: int, first_name: str, 
                   last_name: str, username: str):
    try:
        user = User(user_id=user_id, first_name=first_name, 
                    last_name=last_name, username=username)
        await user.create()
    except UniqueViolationError:
        print('Користувача не додано')

async def check_chat_user(message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user.is_bot:
            if await select_user(message.reply_to_message.from_user.id) is None:
                await add_user(message.reply_to_message.from_user.id,
                               message.reply_to_message.from_user.first_name,
                               message.reply_to_message.from_user.last_name,
                               message.reply_to_message.from_user.username)
            else:
                pass
    else:
        if not message.from_user.is_bot:
            if await select_user(message.from_user.id) is None:
                await add_user(message.from_user.id,
                               message.from_user.first_name,
                               message.from_user.last_name,
                               message.from_user.username)
            else:
                pass

async def select_all_users():
    users = await users.query.gino.all()
    return users

async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count

async def select_user(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user

async def update_status(user_id: int, status: str):
    user = await select_user(user_id)
    await user.update(status=status).apply()

async def update_info(user_id: int, first_name: str, last_name: str, 
                      username: str):
    user = await select_user(user_id)
    await user.update(first_name=first_name).apply()
    await user.update(last_name=last_name).apply()
    await user.update(username=username).apply()
    count = int(user.count_message) + 1
    await user.update(count_message=count).apply()