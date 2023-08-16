from aiogram import types
from loader import dp, bot
from filters import IsGroup
from utils.db_api import rules_commands
from aiogram.dispatcher.filters import Text
from utils.db_api import quick_commands as sql_commands
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.message_handler(IsGroup(), commands=['rmrules'])
async def remove_rules(message: types.Message):

    await sql_commands.check_chat_user(message)
    await sql_commands.update_info(message.from_user.id,
                                   message.from_user.first_name,
                                   message.from_user.last_name,
                                   message.from_user.username)
    
    try:
        user = await sql_commands.select_user(message.from_user.id)
        if user.status == 'banned':
            await message.reply(f'{message.from_user.first_name} ти у чорному списку')

        elif user.status == 'active':
            chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            if chat_member.status == types.ChatMemberStatus.OWNER:
                owner = message.from_user.id
                if await rules_commands.select_chat(chat_id=message.chat.id) is None:
                    await message.reply(f'{message.from_user.get_mention(as_html=True)} поки що немає правил ❗️')
                else:
                    accept_remove = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text='Так', callback_data=f'rmrule#{owner}'),
                                                    InlineKeyboardButton(text='Ні', callback_data=f'cancel_rm#{owner}')
                                                ]
                                            ])
                    await message.reply(f'{message.from_user.get_mention(as_html=True)}'
                                        f', ви впевнені що хочите видалити правила ?', 
                                        reply_markup=accept_remove)
                    
    except Exception as _ex:
            print(f'[ERROR] {_ex}')


@dp.callback_query_handler(Text(startswith='rmrule#'))
async def accept_rm(c: types.CallbackQuery):
    try:
        user = await sql_commands.select_user(c.from_user.id)
        if user.status == 'banned':
            await c.message.reply(f'{c.from_user.first_name} ти у чорному списку')

        elif user.status == 'active':
            if c.data == f'rmrule#{c.from_user.id}':
                await rules_commands.delete_rule(chat_id=c.message.chat.id)
                await c.message.edit_text(f'{c.from_user.get_mention(as_html=True)}, правила видалені ❗️')
            else:
                await bot.answer_callback_query(c.id, text=f'Ця кнопка не для вас !', show_alert=True)

    except Exception as _ex:
            print(f'[ERROR] {_ex}')

@dp.callback_query_handler(Text(startswith='cancel#'))
async def decline_rm(c: types.CallbackQuery):
    try:
        user = await sql_commands.select_user(c.from_user.id)
        if user.status == 'banned':
            await c.message.reply(f'{c.from_user.first_name} ти у чорному списку')

        elif user.status == 'active':
            if c.data == f'cancel_rm#{c.from_user.id}':
                await c.message.edit_text(f'{c.from_user.get_mention(as_html=True)}, правила не видалені ❗️')
            else:
                await bot.answer_callback_query(c.id, text=f'Ця кнопка не для вас !', show_alert=True)
    except Exception as _ex:
            print(f'[ERROR] {_ex}')