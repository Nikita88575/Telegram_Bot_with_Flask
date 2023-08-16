from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Початок"),
        types.BotCommand("stat", "Статистика"),
        types.BotCommand("info", "Інформація"),
        types.BotCommand("help", "Допомога")
    ])