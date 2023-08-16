async def on_startup(dp):
    import filters
    filters.private_chat.setup(dp)
    #filters.group_chat.setup(dp)
    #filters.group_admin.setup(dp)
    import middlewares
    middlewares.setup(dp)
    from utils.notify_admins import on_startup_notify
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)
    await on_startup_notify(dp)
    print("Я живий")

    from loader import db
    from utils.db_api.db_gino import on_startup
    print('Підключення до PostgreSQL')
    await on_startup(dp)

    # print('Видалення таблиць')
    # await db.gino.drop_all()

    print('Створення таблиць')
    await db.gino.create_all()
    print('Готово')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)