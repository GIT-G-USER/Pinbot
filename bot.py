"""Telegram bot: /zakrep pins the replied-to message without unpinning others."""

import asyncio
import logging
import os

from telegram import Update
from telegram.constants import ChatType
from telegram.error import BadRequest, Forbidden
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def nachatzakrep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Привет! Ответь на сообщение командой /zakrep — я закреплю его, "
        "не снимая уже закреплённые.\n"
        "/otkrep — открепить сообщение, на которое ответил.\n"
        "/spisok — показать текущее закреплённое сообщение."
    )


async def zakrep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    target = message.reply_to_message
    if target is None:
        await message.reply_text("Ответь этой командой на сообщение, которое нужно закрепить.")
        return

    silent = bool(set(context.args) & {"tiho", "silent", "тихо"})

    try:
        await context.bot.pin_chat_message(
            chat_id=message.chat_id,
            message_id=target.message_id,
            disable_notification=silent,
        )
    except (BadRequest, Forbidden) as exc:
        logger.warning("pin failed in chat %s: %s", message.chat_id, exc)
        await message.reply_text(
            "Не смог закрепить. Проверь, что я админ и у меня есть право "
            f"«Закреплять сообщения». Ошибка: {exc.message}"
        )
        return

    await message.reply_text("Закрепил. Старые закреплённые сообщения не тронуты.")


async def otkrep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    target = message.reply_to_message
    if target is None:
        await message.reply_text("Ответь этой командой на закреплённое сообщение.")
        return

    try:
        await context.bot.unpin_chat_message(
            chat_id=message.chat_id, message_id=target.message_id
        )
    except (BadRequest, Forbidden) as exc:
        await message.reply_text(f"Не смог открепить: {exc.message}")
        return

    await message.reply_text("Открепил только это сообщение.")


async def spisok(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = await context.bot.get_chat(update.effective_chat.id)
    pinned = chat.pinned_message
    if pinned is None:
        await update.effective_message.reply_text("Закреплённых сообщений нет.")
        return

    link = None
    if chat.username:
        link = f"https://t.me/{chat.username}/{pinned.message_id}"
    elif chat.type in (ChatType.SUPERGROUP, ChatType.CHANNEL):
        link = f"https://t.me/c/{str(chat.id).removeprefix('-100')}/{pinned.message_id}"

    text = f"Последнее закреплённое: #{pinned.message_id}"
    if link:
        text += f"\n{link}"
    text += "\nОстальные закреплённые смотри в списке закреплённых Telegram."
    await update.effective_message.reply_text(text)


# Вставь сюда токен от @BotFather (или задай переменную окружения TELEGRAM_BOT_TOKEN)
TOKEN = "СЮДА_ВСТАВЬ_ТОКЕН"


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or TOKEN
    if not token or token == "СЮДА_ВСТАВЬ_ТОКЕН":
        raise SystemExit("Впиши токен в переменную TOKEN в начале файла")

    asyncio.set_event_loop(asyncio.new_event_loop())

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("nachatzakrep", nachatzakrep))
    app.add_handler(CommandHandler("zakrep", zakrep))
    app.add_handler(CommandHandler("otkrep", otkrep))
    app.add_handler(CommandHandler("spisok", spisok))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
