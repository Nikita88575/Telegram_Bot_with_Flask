from loader import dp
from aiogram import types
from utils.db_api import quick_commands as sql_commands

@dp.message_handler(commands=['help'])
async def shrug(message: types.Message):
    await sql_commands.update_info(user_id=message.from_user.id,
                                   first_name=message.from_user.first_name,
                                   last_name=message.from_user.last_name,
                                   username=message.from_user.username)
    
    try:
        user = await sql_commands.select_user(message.from_user.id)
        if user.status == 'banned':
            await message.reply(f'{message.from_user.first_name} ти у чорному списку')

        elif user.status == 'active':
            await message.reply(
                '<b>Базові команди</b>\n\n'
                '👮🏻‍♂️ Доступно для адміністраторів\n'
                '👥 Доступно для всіх\n\n'

                '👮🏻‍♂️ <code>/ban</code> - дозволяє заблокувати користувача в групі, не даючи '
                'йому можливості приєднатися знову, використовуючи посилання групи.\n\n'

                '👮🏻‍♂️ <code>/unban</code> - дозволяє видалити користувача з чорного списку '
                'групи, надавши можливість знову приєднатися за посиланням групи.\n\n'
                
                '👮🏻‍♂️ <code>/kick</code> - блокує користувача з групи, даючи можливість знову'
                ' приєднатися за посиланням групи.\n\n'

                '👮🏻‍♂️ <code>/mute</code> - переводить користувача в режим '
                '<i>тільки для читання</i>. Він може читати, але не може '
                'надсилати повідомлення.\n\n'

                '👮🏻‍♂️ <code>/unmute</code> - повертає користувачу можливість відправляти '
                'повідомлення.\n\n'

                '👥 <code>/rules</code> - дозволяє дізнатися правила групи (для всіх). '
                'Дозволяє додати та оновити правила групи (Тільки для адміністраторів).\n\n'

                '👮🏻‍♂️ <code>/rmrules</code> - видаляє правила групи.\n\n'
                
                '👥 <code>/info</code> - надає інформацію про користувача.\n\n'
                
                '👥 <code>/stat</code> - надає статистику про користувача.\n\n'
                
                '👥 <code>/settings</code> - налаштування.\n\n')
            
    except Exception as _ex:
        print(f'[ERROR] {_ex}')