from aiogram import Dispatcher
from .bot_join import IsBotJoined
from .bot_left import IsBotLeft
from .private_chat import IsPrivate
from .group_chat import IsGroup
from .group_admin import IsAdmin
from .chat_owner import IsOwner
from .bot_owner import IsBotOwner

def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsOwner)
    dp.filters_factory.bind(IsBotJoined)
    dp.filters_factory.bind(IsBotLeft)
    dp.filters_factory.bind(IsBotOwner)