from aiogram import types
from loader import dp, bot
from filters import IsGroup
from utils.db_api import rules_commands
from utils.db_api import quick_commands as sql_commands

@dp.message_handler(IsGroup(), commands=['rules'])
async def rules(message: types.Message):
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
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

            if chat_member.status == types.ChatMemberStatus.OWNER:
                if await rules_commands.select_chat(message.chat.id) is None:

                    if message.html_text == '/rules@pi666_bot' or message.html_text == '/rules':
                        await message.reply(f'{message.from_user.get_mention(as_html=True)}, '
                                                f'поки що немає правил ❗️')
                        
                    elif message.html_text.startswith('/rules@pi666_bot'):
                        await rules_commands.add_rules(message.chat.id, 
                        rules=message.html_text.split('/rules@pi666_bot')[1])
                        await message.reply(f'{message.from_user.get_mention(as_html=True)}, '
                                            f'правила успішно додані ❗️')
                        
                    elif message.html_text.startswith('/rules'):
                        await rules_commands.add_rules(message.chat.id, 
                                                    message.html_text.split('/rules')[1])
                        await message.reply(f'{message.from_user.get_mention(as_html=True)}, '
                                            f'правила успішно додані ❗️')
                        
                else:
                    if message.html_text == '/rules@pi666_bot' or message.html_text == '/rules':
                        chat_rule = await rules_commands.select_chat(message.chat.id)
                        us = message.from_user.get_mention(as_html=True, name="Правила чату")
                        await message.reply(f'❗️❗️❗️{us}❗️❗️❗️\n{chat_rule.rules}')

                    else:
                        if message.html_text.startswith('/rules@pi666_bot'):
                            await rules_commands.update_rules(message.chat.id, 
                            new_rules=message.html_text.split('/rules@pi666_bot')[1])
                            await message.reply(f'{message.from_user.get_mention(as_html=True)}, правила оновлені ❗️')

                        elif message.html_text.startswith('/rules'):
                            await rules_commands.update_rules(message.chat.id, 
                                                            message.html_text.split('/rules')[1])
                            await message.reply(f'{message.from_user.get_mention(as_html=True)}, правила оновлені ❗️')
            
            else:
                if await rules_commands.select_chat(message.chat.id) is None:
                    await message.reply(f'{message.from_user.get_mention(as_html=True)} поки що немає правил ❗️')

                else:
                    chat_rule = await rules_commands.select_chat(message.chat.id)
                    us = message.from_user.get_mention(as_html=True, name="Правила чату")
                    await message.reply(f'!!!{us}!!!\n{chat_rule.rules}')
    
    except Exception as _ex:
            print(f'[ERROR] {_ex}')