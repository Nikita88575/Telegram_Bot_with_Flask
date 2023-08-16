from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter

class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)