import aiosqlite
from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("report"))
async def report(message: Message, bot: Bot):
    
    logger.info(f"[REPORT] Команда получена от {message.from_user.id}")
    logger.info(f"[REPORT] reply_to_message: {message.reply_to_message}")
    
    # Проверка 1: есть ли вообще ответ
    if not message.reply_to_message:
        logger.warning(f"[REPORT] Нет reply_to_message")
        return await message.answer("❌ Ты не ответил на сообщение.")
    
    logger.info(f"[REPORT] Ответ найден: сообщение ID {message.reply_to_message.message_id}")
    
    replied = message.reply_to_message
    chat = message.chat
    
    try:
        # Тестовое сообщение
        test_msg = await bot.send_message(
            chat_id=-1003908585715, 
            text=f"⚠ Репорт от @{message.from_user.username or message.from_user.id}\n"
        )
        logger.info(f"[REPORT] Тестовое сообщение отправлено: {test_msg.message_id}")
        
        # Пересылка
        forwarded = await bot.forward_message(
            chat_id=-1003908585715,
            from_chat_id=replied.chat.id,
            message_id=replied.message_id
        )
        logger.info(f"[REPORT] Сообщение переслано: {forwarded.message_id}")
        
        await message.answer("✅ Отчёт отправлен.", parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"[REPORT] Ошибка: {type(e).__name__}: {e}")
        await message.answer(
            f"❌ Ошибка отправки репорта\n\n"
            f"<code>{type(e).__name__}: {str(e)[:100]}</code>",
            parse_mode="HTML"
        )