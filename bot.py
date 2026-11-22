"""ILMORA TECH — ma'lumot bot (aiogram 3).

Ishga tushirish:
    pip install aiogram==3.*
    BOT_TOKEN=... python bot.py        (Windows: set BOT_TOKEN=...  keyin  python bot.py)
"""
import asyncio
import logging
import os
import re

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (BotCommand, CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton, Message,
                           ReplyKeyboardMarkup)

# ---- Sozlamalar (shu yerni o'zgartirasiz) ----
ADMIN_USERNAME = "Muhammadulloh77"
INSTAGRAM_URL = "https://www.instagram.com/ilmora.tech"
SITE_URL = ""      # sayt Netlify'ga qo'yilgach havolani yozing, masalan "https://ilmora-tech.netlify.app"
CHANNEL_URL = "https://t.me/ilmoratech"

ADMIN_URL = f"https://t.me/{ADMIN_USERNAME}"

SERVICES = {
    "smm": ("📈 SMM",
            "Instagram va Telegram sahifangizni yuritamiz.\n\n"
            "• Kontent-reja va post dizayni\n• Storis va Reels\n• Target reklama\n• Oylik statistika va hisobot"),
    "bot": ("🤖 Telegram botlar",
            "Biznesingiz uchun ishlaydigan botlar.\n\n"
            "• Buyurtma va katalog botlari\n• Ro'yxatga olish va so'rovnoma\n• To'lov va admin panel\n• 24/7 avtomatik javob"),
    "web": ("🌐 Veb-saytlar",
            "Telefon va kompyuterga moslashgan zamonaviy saytlar.\n\n"
            "• Landing sahifalar\n• Korporativ saytlar\n• Internet-do'konlar\n• Telegram bilan ulash"),
    "video": ("🎬 AI videolar",
              "Sun'iy intellekt yordamida reklama va kontent videolari.\n\n"
              "• Ssenariy va ovoz\n• Reels / Shorts formatlari\n• Mahsulot va xizmat reklamasi"),
    "logo": ("✨ Logotiplar",
             "Brendingizni eslab qolinadigan logotiplar.\n\n"
             "• Bir nechta variant\n• Barcha formatlarda fayllar\n• Rang va shrift tanlovi"),
    "design": ("🎨 Kreativ dizayn",
               "Ijtimoiy tarmoq va reklama uchun dizaynlar.\n\n"
               "• Post va banner\n• Flayer va vizitka\n• Brend uslubi"),
}

WELCOME = (
    "Assalomu alaykum, {name}! 👋\n\n"
    "<b>ILMORA TECH</b> — biznesingizni internetda o'stiramiz.\n"
    "SMM • Telegram botlar • Saytlar • AI videolar • Logo va dizayn\n\n"
    "Pastdagi tugmalardan birini tanlang 👇"
)

PRICES = (
    "💰 <b>Narxlar</b>\n\n"
    "Narx ish hajmi va muddatiga bog'liq. Vazifangizni yozing — "
    "aniq narx va muddatni tez aytib beramiz."
)

ABOUT = (
    "ℹ️ <b>ILMORA TECH haqida</b>\n\n"
    "Biz SMM, Telegram botlar, saytlar, AI videolar va dizayn bilan shug'ullanamiz. "
    "Har bir loyihani sizning maqsadingizdan boshlaymiz: ko'proq mijoz, qulay savdo yoki kuchli brend.\n\n"
    "<b>Qanday ishlaymiz:</b>\n"
    "1. Suhbat — maqsad va budjetni aniqlaymiz\n"
    "2. Reja va narx — muddat va narxni kelishamiz\n"
    "3. Ish — variantlarni ko'rsatib, tuzatib boramiz\n"
    "4. Topshirish — tayyor natija va qo'llab-quvvatlash"
)

CONTACT = (
    "📩 <b>Bog'lanish</b>\n\n"
    f"Telegram: @{ADMIN_USERNAME}\n"
    "Instagram: @ilmora.tech\n\n"
    "Yozing — tez javob beramiz!"
)


BTN_SERVICES = "🛠 Xizmatlar"
BTN_PRICES = "💰 Narxlar"
BTN_WORKS = "📸 Ishlarimiz"
BTN_CONTACT = "📩 Bog'lanish"


def reply_menu() -> ReplyKeyboardMarkup:
    """Pastdagi klaviatura o'rniga chiqadigan 4 ta doimiy tugma."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_SERVICES), KeyboardButton(text=BTN_PRICES)],
            [KeyboardButton(text=BTN_WORKS), KeyboardButton(text=BTN_CONTACT)],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Bo'limni tanlang 👇",
    )


WORKS = (
    "📸 <b>Ishlarimiz</b>\n\n"
    "Qilgan ishlarimiz — postlar, logotiplar, videolar va botlar — "
    "Instagram sahifamiz va Telegram kanalimizda."
)


def works_menu() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text="📸 Instagram", url=INSTAGRAM_URL)]]
    if CHANNEL_URL:
        rows.append([InlineKeyboardButton(text="📢 Telegram kanal", url=CHANNEL_URL)])
    if SITE_URL:
        rows.append([InlineKeyboardButton(text="🌐 Sayt", url=SITE_URL)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def contact_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Adminga yozish", url=ADMIN_URL)],
    ])


def main_menu() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="🛠 Xizmatlar", callback_data="services")],
        [InlineKeyboardButton(text="💰 Narxlar", callback_data="prices"),
         InlineKeyboardButton(text="ℹ️ Biz haqimizda", callback_data="about")],
        [InlineKeyboardButton(text="📸 Ishlarimiz (Instagram)", url=INSTAGRAM_URL)],
    ]
    extra = []
    if SITE_URL:
        extra.append(InlineKeyboardButton(text="🌐 Sayt", url=SITE_URL))
    if CHANNEL_URL:
        extra.append(InlineKeyboardButton(text="📢 Kanal", url=CHANNEL_URL))
    if extra:
        rows.append(extra)
    rows.append([InlineKeyboardButton(text="📩 Bog'lanish", callback_data="contact")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def services_menu() -> InlineKeyboardMarkup:
    items = list(SERVICES.items())
    rows = [[InlineKeyboardButton(text=items[i][1][0], callback_data=f"svc:{items[i][0]}"),
             InlineKeyboardButton(text=items[i + 1][1][0], callback_data=f"svc:{items[i + 1][0]}")]
            for i in range(0, len(items) - 1, 2)]
    if len(items) % 2:
        k, (t, _) = items[-1]
        rows.append([InlineKeyboardButton(text=t, callback_data=f"svc:{k}")])
    rows.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="home")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def back_with_order(back_to: str = "home") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Admin bilan bog'lanish", url=ADMIN_URL)],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data=back_to)],
    ])


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    name = message.from_user.first_name if message.from_user else "do'st"
    await message.answer(WELCOME.format(name=name), reply_markup=reply_menu())


@dp.message(Command("xizmatlar"))
async def cmd_services(message: Message) -> None:
    await message.answer("🛠 <b>Xizmatlarimiz</b>\n\nQaysi biri qiziqtiradi?", reply_markup=services_menu())


@dp.message(Command("aloqa"))
async def cmd_contact(message: Message) -> None:
    await message.answer(CONTACT, reply_markup=contact_menu())


@dp.callback_query(F.data == "home")
async def cb_home(call: CallbackQuery) -> None:
    # Bosh menyu endi pastdagi tugmalarda, shuning uchun inline xabarni yopamiz
    await call.message.edit_text("Pastdagi tugmalardan birini tanlang 👇")
    await call.answer()


@dp.callback_query(F.data == "services")
async def cb_services(call: CallbackQuery) -> None:
    await call.message.edit_text("🛠 <b>Xizmatlarimiz</b>\n\nQaysi biri qiziqtiradi?", reply_markup=services_menu())
    await call.answer()


@dp.callback_query(F.data.startswith("svc:"))
async def cb_service(call: CallbackQuery) -> None:
    key = call.data.split(":", 1)[1]
    if key not in SERVICES:
        await call.answer()
        return
    title, text = SERVICES[key]
    await call.message.edit_text(f"<b>{title}</b>\n\n{text}", reply_markup=back_with_order("services"))
    await call.answer()


@dp.callback_query(F.data.in_({"prices", "about", "contact"}))
async def cb_pages(call: CallbackQuery) -> None:
    text = {"prices": PRICES, "about": ABOUT, "contact": CONTACT}[call.data]
    await call.message.edit_text(text, reply_markup=back_with_order())
    await call.answer()


@dp.message(F.text == BTN_SERVICES)
async def btn_services(message: Message) -> None:
    await message.answer("🛠 <b>Xizmatlarimiz</b>\n\nQaysi biri qiziqtiradi?", reply_markup=services_menu())


@dp.message(F.text == BTN_PRICES)
async def btn_prices(message: Message) -> None:
    await message.answer(PRICES, reply_markup=contact_menu())


@dp.message(F.text == BTN_WORKS)
async def btn_works(message: Message) -> None:
    await message.answer(WORKS, reply_markup=works_menu())


@dp.message(F.text == BTN_CONTACT)
async def btn_contact(message: Message) -> None:
    await message.answer(CONTACT, reply_markup=contact_menu())


@dp.message()
async def fallback(message: Message) -> None:
    await message.answer("Pastdagi tugmalardan birini tanlang 👇", reply_markup=reply_menu())


async def main() -> None:
    raw = os.getenv("BOT_TOKEN", "")
    # Nusxalashda qo'shilib qolgan bo'sh joy yoki ortiqcha matnni tozalaymiz
    found = re.search(r"\d{5,}:[A-Za-z0-9_-]{30,}", raw)
    token = found.group(0) if found else raw.strip()
    if not token:
        raise SystemExit("BOT_TOKEN topilmadi. BotFather bergan tokenni BOT_TOKEN sifatida kiriting.")
    from aiogram.client.default import DefaultBotProperties
    bot = Bot(token, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.set_my_commands([
        BotCommand(command="start", description="Bosh menyu"),
        BotCommand(command="xizmatlar", description="Xizmatlarimiz"),
        BotCommand(command="aloqa", description="Bog'lanish"),
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
