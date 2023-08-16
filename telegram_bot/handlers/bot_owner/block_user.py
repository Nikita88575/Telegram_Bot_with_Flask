# import re
# from loader import dp
# from aiogram import types
# from filters import IsBotOwner
# from utils.db_api import block_tag_commands as block

# @dp.message_handler(IsBotOwner(), commands=['blocktag'])
# async def dice(message: types.Message):
#     try:
#        await block.block_tag(tag=message.html_text.split()[1])
#        await message.reply(f'Тег {message.html_text.split()[1]} заблокованно')
#     except Exception as _ex:
#         #pass
#         print(f'[ERROR] {_ex}')