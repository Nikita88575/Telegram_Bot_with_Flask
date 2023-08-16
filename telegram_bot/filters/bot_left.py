from aiogram import types 
from aiogram.dispatcher.filters import BoundFilter
from loader import dp

class IsBotLeft(BoundFilter):
    """
    The filter works when the bot lefts to a group
    """
    async def check(self, message: types.Message):

        bot_id = (await dp.bot.get_me())["id"]
        user_id = message.left_chat_member["id"]

        if bot_id == user_id:
            return True
        return False