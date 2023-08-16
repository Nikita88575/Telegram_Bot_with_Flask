from aiogram import types 
from aiogram.dispatcher.filters import BoundFilter
from loader import bot
from data.config import admin_id

class IsBotOwner(BoundFilter):
    async def check(self, message: types.Message):
        chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if chat_member.user.id == admin_id[0]:
            return chat_member