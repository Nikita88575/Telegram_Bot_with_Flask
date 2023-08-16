from aiogram.types import Message, ChatMemberStatus
from loader import bot, dp
from filters import IsGroup
from utils.db_api import group_settings as settings

@dp.message_handler(IsGroup(), )
async def links(message: Message):
    for links in message.entities:
        if links.type in ['url', 'text_link']:
            chat = await settings.select_chat(message.chat.id)

            if chat.delete_link == True:

                is_admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
                if is_admin.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:

                    if chat.delete_admins_link == True:    
                        await message.delete()

                    else:
                        pass

                else:
                    await message.delete()

            else:
                pass
                    
        else:
            pass