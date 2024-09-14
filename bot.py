import asyncio
import logging
import sys
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Загрузка конфигурации
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Bot token
TOKEN = config["TOKEN"]

# Dispatcher initialization
dp = Dispatcher()

# Хранилище состояний для пользователей (для отслеживания текущего уровня меню)
user_states = {}


# Функция для генерации клавиатуры на основе переданного меню
def generate_keyboard(buttons, add_back=False):
    keyboard = InlineKeyboardBuilder()

    # Если нужно добавить кнопку "Назад", делаем это первой
    if add_back:
        keyboard.button(text="◀ Назад", callback_data="back")

    # Добавляем остальные кнопки
    for button in buttons:
        keyboard.button(text=button, callback_data=button)

    # Устанавливаем максимум по 3 кнопки в ряд
    keyboard.adjust(3)

    # Проверяем, есть ли кнопки в клавиатуре
    if not keyboard.buttons:
        return None

    # Возвращаем объект InlineKeyboardMarkup
    return keyboard.as_markup()


# Получение текущего меню для пользователя
def get_current_menu(user_id):
    current_path = user_states.get(
        user_id, ["menu"]
    )  # Если состояние не задано, возвращаем верхний уровень
    current_menu = config
    for key in current_path[1:]:
        if "menu" in current_menu and key in current_menu["menu"]:
            current_menu = current_menu["menu"][key]
        else:
            break
    return current_menu


# Стартовое сообщение с выбором категории
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    user_states[message.from_user.id] = [
        "menu"
    ]  # Инициализируем состояние пользователя
    current_menu = get_current_menu(message.from_user.id)

    keyboard = generate_keyboard(current_menu.get("menu", {}).keys())

    if keyboard:
        await message.answer(config["welcome_message"], reply_markup=keyboard)
    else:
        await message.answer(config["welcome_message"])


# Обработка нажатия кнопок
@dp.callback_query(F.data)
async def callback_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data

    if data == "back":  # Обработка кнопки "Назад"
        if len(user_states[user_id]) > 1:
            user_states[user_id].pop()  # Возвращаемся на уровень выше
        current_menu = get_current_menu(user_id)
        keyboard = generate_keyboard(
            current_menu.get("menu", {}).keys(), add_back=len(user_states[user_id]) > 1
        )
        if keyboard:
            await callback.message.edit_text(
                current_menu.get("description", "Меню"), reply_markup=keyboard
            )
        else:
            await callback.message.edit_text(current_menu.get("description", "Меню"))
        return

    # Обновляем состояние пользователя
    user_states[user_id].append(data)
    current_menu = get_current_menu(user_id)

    # Получаем клавиатуру для текущего меню
    keyboard = generate_keyboard(current_menu.get("menu", {}).keys(), add_back=True)

    # Отправляем описание текущего меню и клавиатуру
    if keyboard:
        await callback.message.edit_text(
            current_menu.get("description", "Меню"), reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(current_menu.get("description", "Меню"))


# Основная функция
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
