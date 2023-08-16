from aiogram import types
from loader import dp, bot
from filters import IsGroup, IsAdmin
from aiogram.dispatcher.filters import Text
from utils.db_api import group_settings as settings
from utils.db_api import quick_commands as sql_commands
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.message_handler(IsGroup(), IsAdmin(), commands=['settings'])
async def setup(message: types.Message):
    await sql_commands.check_chat_user(message)
    # await sql_commands.update_info(message.from_user.id,
    #                                message.from_user.first_name,
    #                                message.from_user.last_name,
    #                                message.from_user.username)

    if await settings.select_chat(message.chat.id) is None:
        await settings.add_chat_settings(message.chat.id, message.chat.full_name)
    
    admin = message.from_user.id
    chat = await settings.select_chat(message.chat.id)
        
    if chat.delete_link == True:
        delete_link_status = '✅'
    else:
        delete_link_status = '❌'

    if chat.delete_admins_link == True:
        delete_admins_link_status = '✅'
    else:
        delete_admins_link_status = '❌'

    setup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=f'Видаляти посилання {delete_link_status}', 
                                                             callback_data=f'Edit_del_link_status#{admin}')
                                    ],
                                    [
                                        InlineKeyboardButton(text=('Видаляти посилання адміністраторів ' 
                                                                   f'{delete_admins_link_status}'),
                                                             callback_data=f'Edit_link_for_admins_staus#{admin}')
                                    ],
                                    [
                                        InlineKeyboardButton(text=f'Закрити', 
                                                             callback_data=f'Close_group_settings#{admin}')
                                    ]
                                ])
        
    await message.reply(f'{message.from_user.get_mention("Налаштування", True)}', reply_markup=setup)

@dp.callback_query_handler(Text(startswith='Edit_del_link_status#'))
async def delete_links(c: types.CallbackQuery):
    try:
        user = await sql_commands.select_user(c.from_user.id)
        if user.status == 'banned':
            await c.message.reply(f'{c.from_user.first_name} ти у чорному списку')

        elif user.status == 'active':

            if c.data == f'Edit_del_link_status#{c.from_user.id}':
                chat = await settings.select_chat(c.message.chat.id)

                if chat.delete_link == True:
                    await settings.update_delete_links(c.message.chat.id, False)
                    await settings.update_delete_links_for_admin(c.message.chat.id, False)
                else:
                    await settings.update_delete_links(c.message.chat.id, True)

                chat = await settings.select_chat(c.message.chat.id)
        
                if chat.delete_link == True:
                    delete_link_status = '✅'
                else:
                    delete_link_status = '❌'

                if chat.delete_admins_link == True:
                    delete_admins_link_status = '✅'
                else:
                    delete_admins_link_status = '❌'

                admin = c.from_user.id
                setup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=f'Видаляти посилання {delete_link_status}', 
                                                             callback_data=f'Edit_del_link_status#{admin}')
                                    ],
                                    [
                                        InlineKeyboardButton(text=('Видаляти посилання адміністраторів ' 
                                                                   f'{delete_admins_link_status}'),
                                                             callback_data=f'Edit_link_for_admins_staus#{admin}')
                                    ],
                                    [
                                        InlineKeyboardButton(text=f'Закрити', 
                                                             callback_data=f'Close_group_settings#{admin}')
                                    ]
                                ])
                await c.message.edit_reply_markup(setup)

            else:
                await bot.answer_callback_query(c.message.chat.id, text=f'Ця кнопка не для вас !', show_alert=True)

    except Exception as _ex:
            print(f'[ERROR] {_ex}')

@dp.callback_query_handler(Text(startswith='Edit_link_for_admins_staus#'))
async def delete_admins_links(c: types.CallbackQuery):
    try:
        user = await sql_commands.select_user(c.from_user.id)
        if user.status == 'banned':
            await c.message.reply(f'{c.from_user.first_name} ти у чорному списку')

        elif user.status == 'active':

            if c.data == f'Edit_link_for_admins_staus#{c.from_user.id}':
                chat = await settings.select_chat(c.message.chat.id)

                if chat.delete_link == True:

                    if chat.delete_admins_link == False:
                        await settings.update_delete_links_for_admin(c.message.chat.id, True)
                    else:
                        await settings.update_delete_links_for_admin(c.message.chat.id, False)

                chat = await settings.select_chat(c.message.chat.id)
        
                if chat.delete_link == True:
                    delete_link_status = '✅'
                else:
                    delete_link_status = '❌'

                if chat.delete_admins_link == True:
                    delete_admins_link_status = '✅'
                else:
                    delete_admins_link_status = '❌'

                admin = c.from_user.id
                setup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text=f'Видаляти посилання {delete_link_status}', 
                                                             callback_data=f'Edit_del_link_status#{admin}')
                                    ],
                                    [
                                        InlineKeyboardButton(text=('Видаляти посилання адміністраторів ' 
                                                                   f'{delete_admins_link_status}'),
                                                             callback_data=f'Edit_link_for_admins_staus#{admin}')
                                    ],
                                    [
                                        InlineKeyboardButton(text=f'Закрити', 
                                                             callback_data=f'Close_group_settings#{admin}')
                                    ]

                                ])

                await c.message.edit_reply_markup(setup)
            else:
                await bot.answer_callback_query(c.message.chat.id, text=f'Ця кнопка не для вас !', show_alert=True)

    except Exception as _ex:
            print(f'[ERROR] {_ex}')

@dp.callback_query_handler(Text(startswith='Close_group_settings#'))
async def accept_rm(c: types.CallbackQuery):
    try:
        user = await sql_commands.select_user(c.from_user.id)
        if user.status == 'banned':
            await c.message.reply(f'{c.from_user.first_name} ти у чорному списку')

        elif user.status == 'active':

            if c.data == f'Close_group_settings#{c.from_user.id}':
                await c.message.delete()
            else:
                await bot.answer_callback_query(c.message.chat.id, text=f'Ця кнопка не для вас !', show_alert=True)

    except Exception as _ex:
            print(f'[ERROR] {_ex}')