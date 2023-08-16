from aiogram import types 
from aiogram.dispatcher.filters import BoundFilter
from loader import bot  

class IsOwner(BoundFilter):
    async def check(self, message: types.Message):
        chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        owner_types =  [types.ChatMemberStatus.OWNER]
        return chat_member.status in owner_types