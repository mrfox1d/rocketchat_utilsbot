import aiosqlite
from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import asyncio

router = Router()

@router.message(Command("report") | (F.text.lower() == "репорт"))
async def report(message: Message, bot: Bot):

    if not message.reply_to_message:
        return await message.answer("❌ Ты не ответил на сообщение.")

    replied = message.reply_to_message
    chat = message.chat

    admins = await bot.get_chat_administrators(chat_id=message.chat.id)

    for admin in admins:
        if admin.user.is_bot:
            continue

        try:
            await bot.send_message(chat_id=admin.user.id, text=f"⚠ Репорт от юзера @{message.from_user.username} в рокет чате:")

            await message.bot.forward_message(chat_id=admin.user.id,
                                            from_chat_id=replied.chat.id,
                                            message_id=replied.message_id
                                            )
        except Exception as e:
            await message.answer(f"❌ Не удалось отправить репорт администратору @{admin.user.username}.\n\n"
                                 f"⚠ Ошибка:\n"
                                 f"<pre><code class='language-python'>{e}</code></pre>\n\n"
                                 f"❓ Не нашли ошибку в /faq? Лучше пишите @mrfox1dddd!")
        
    msg = await message.answer("<i>✅ Отчёт отправлен.</i>", parse_mode="HTML")
    asyncio.sleep(5)
    await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)