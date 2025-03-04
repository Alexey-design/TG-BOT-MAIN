import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
API_TOKEN = '7251257913:AAEX_l3ExUxT-Epz8zr-0ScBjs9tOF_bqDo'  # Замените на ваш токен
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Состояния для хранения данных
class TaskState(StatesGroup):
    waiting_for_task_number = State()
    waiting_for_task_action = State()

class ProgrammingState(StatesGroup):
    waiting_for_language = State()
    waiting_for_section = State()
    waiting_for_theory_level = State()

# Доступные дни недели и временные слоты
week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
time_slots = [f"{hour}:00-{hour+1}:00" for hour in range(15, 22)]

# Команда /start
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Подготовка к ЕГЭ")],
            [types.KeyboardButton(text="Подготовка к ОГЭ")],
            [types.KeyboardButton(text="Тренировка программирования")],
            [types.KeyboardButton(text="Записаться на занятие")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите вариант:", reply_markup=keyboard)

# Функция для возврата назад
@dp.message(lambda message: message.text == "Назад")
async def handle_back(message: Message) -> None:
    await command_start_handler(message)

# Обработка выбора подготовки к экзаменам
@dp.message(lambda message: message.text in ["Подготовка к ЕГЭ", "Подготовка к ОГЭ"])
async def handle_exam_preparation(message: Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Информатика")],
            [types.KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Вы выбрали {message.text}. Выберите предмет:", reply_markup=keyboard)

# Обработка выбора Информатики в ЕГЭ
@dp.message(lambda message: message.text == "Информатика")
async def handle_informatics(message: Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Отработать задание")],
            [types.KeyboardButton(text="Решить Вариант")],
            [types.KeyboardButton(text="Информация об экзамене")],
            [types.KeyboardButton(text="База Знаний")],
            [types.KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Обработка выбора "Отработать задание"
@dp.message(lambda message: message.text == "Отработать задание")
async def handle_practice_task(message: Message, state: FSMContext) -> None:
    await message.answer("Введите номер задания (от 1 до 27):")
    await state.set_state(TaskState.waiting_for_task_number)  # Устанавливаем состояние ожидания номера задания

# Обработка ввода номера задания
@dp.message(TaskState.waiting_for_task_number)
async def handle_task_number(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not (1 <= int(message.text) <= 27):
        await message.answer("Пожалуйста, введите число от 1 до 27.")
        return

    task_number = int(message.text)
    await state.update_data(task_number=task_number)  # Сохраняем номер задания

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Информация о задании")],
            [types.KeyboardButton(text="Теория")],
            [types.KeyboardButton(text="Практика")],
            [types.KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Вы выбрали задание №{task_number}. Выберите, что вас интересует:", reply_markup=keyboard)
    await state.set_state(TaskState.waiting_for_task_action)  # Устанавливаем состояние ожидания действия

# Обработка выбора раздела (Информация о задании, Теория, Практика)
@dp.message(TaskState.waiting_for_task_action)
async def handle_task_action(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    task_number = user_data.get("task_number")

    if message.text == "Информация о задании":
        if task_number == 1:
            info = (
                "1. Описание из кодификатора: Умение представлять и считывать данные в разных типах информационных моделей (схемы, карты, таблицы, графики и формулы)\n"
                "2. Уровень сложности задания: Базовый\n"
                "3. Требуется использование специализированного программного обеспечения: Нет\n"
                "4. Макс. балл за выполнение задания: 1\n"
                "5. Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)
        else:
            await message.answer("Информация о задании для этого номера пока недоступна.")

    elif message.text == "Теория":
        if task_number == 1:
            await message.answer("Теория для задания 1: https://skyteach.ru/informatika/ege-po-informatike-teoriya-grafov/")
        else:
            await message.answer("Теория для этого задания пока недоступна.")

    elif message.text == "Практика":
        if task_number == 1:
            practice_links = (
                "Сайт Полякова, генератор по номеру 1:\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=1&answers=on&varId=\n\n"
                "Сложность: Простая\n"
                "https://education.yandex.ru/ege/tasks?task_id=7bea7f84-c854-45ed-ac97-17d7bb823723&category_id=1d59eed0-1914-4f79-9771-5fff8feaf01b&category_id=a3b4e9aa-e02f-4182-8243-eb7841e37706&sort_by=newFirst&level=2&source=all\n\n"
                "Сложность: Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=7bea7f84-c854-45ed-ac97-17d7bb823723&category_id=1d59eed0-1914-4f79-9771-5fff8feaf01b&category_id=a3b4e9aa-e02f-4182-8243-eb7841e37706&sort_by=newFirst&level=4&level=3&source=all\n\n"
                "Сложность: Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=7bea7f84-c854-45ed-ac97-17d7bb823723&category_id=1d59eed0-1914-4f79-9771-5fff8feaf01b&category_id=a3b4e9aa-e02f-4182-8243-eb7841e37706&sort_by=newFirst&level=5&source=all"
            )
            await message.answer(practice_links)
        else:
            await message.answer("Практика для этого задания пока недоступна.")

    elif message.text == "Назад":
        await state.clear()
        await command_start_handler(message)

# Обработка выбора "Решить Вариант"
@dp.message(lambda message: message.text == "Решить Вариант")
async def handle_solve_variant(message: Message) -> None:
    await message.answer("Вы можете выбрать один из вариантов:")
    await message.answer("1. [Вариант Осн 2024](https://bank-ege.ru/ege/informatika/oldVariants/module/10/variant325727)")
    await message.answer("2. [Вариант уровня ЕГЭ](https://bank-ege.ru/ege/informatika/examVariants/variant1?is_my_variants=false)")
    await message.answer("3. [Демо 2025](https://4ege.ru/informatika/71304-demoversija-ege-2025-po-informatike.html)")

# Обработка выбора "Записаться на занятие"
@dp.message(lambda message: message.text == "Записаться на занятие")
async def handle_schedule(message: Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=day)] for day in week_days] + [[types.KeyboardButton(text="Назад")]],
        resize_keyboard=True
    )
    await message.answer("Выберите день недели:", reply_markup=keyboard)

# Обработка выбора дня недели для записи на занятие
@dp.message(lambda message: message.text in week_days)
async def handle_day_selection(message: Message, state: FSMContext) -> None:
    await state.update_data(day=message.text)  # Сохраняем выбранный день
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=slot)] for slot in time_slots] + [[types.KeyboardButton(text="Назад")]],
        resize_keyboard=True
    )
    await message.answer(f"Вы выбрали {message.text}. Выберите временной слот:", reply_markup=keyboard)

# Обработка выбора временного слота
@dp.message(lambda message: message.text in time_slots)
async def handle_time_slot_selection(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    day = user_data.get("day")
    await message.answer(f"Вы записаны на занятие в {day} на {message.text}.")
    await state.clear()  # Очищаем состояние

# Обработка выбора "Тренировка программирования"
@dp.message(lambda message: message.text == "Тренировка программирования")
async def handle_programming_training(message: Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Python")],
            [types.KeyboardButton(text="JavaScript")],
            [types.KeyboardButton(text="C++")],
            [types.KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите язык программирования:", reply_markup=keyboard)
    await state.set_state(ProgrammingState.waiting_for_language)  # Устанавливаем состояние ожидания языка

# Обработка выбора языка программирования
@dp.message(ProgrammingState.waiting_for_language)
async def handle_language_selection(message: Message, state: FSMContext) -> None:
    if message.text not in ["Python", "JavaScript", "C++"]:
        await message.answer("Пожалуйста, выберите язык из предложенных.")
        return

    await state.update_data(language=message.text)  # Сохраняем выбранный язык
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="О разделе")],
            [types.KeyboardButton(text="Теория")],
            [types.KeyboardButton(text="Практика")],
            [types.KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Вы выбрали {message.text}. Выберите раздел:", reply_markup=keyboard)
    await state.set_state(ProgrammingState.waiting_for_section)  # Устанавливаем состояние ожидания раздела

# Обработка выбора раздела (О разделе, Теория, Практика)
@dp.message(ProgrammingState.waiting_for_section)
async def handle_section_selection(message: Message, state: FSMContext) -> None:
    if message.text == "О разделе":
        await message.answer(
            "Уважаемый ученик, если ты пройдешь все уровни с 0 по 4 и преодолеешь все трудности в процессе обучения программированию, "
            "то значительно повысишь свои шансы на успешную сдачу экзамена или реализацию проекта твоей мечты."
        )
    elif message.text == "Теория":
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="1 уровень - Базовые конструкции")],
                [types.KeyboardButton(text="2 уровень - Модули (встроенные в Python)")],
                [types.KeyboardButton(text="3 уровень - Углубление в базовые конструкции")],
                [types.KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True
        )
        await message.answer("Выберите уровень теории:", reply_markup=keyboard)
        await state.set_state(ProgrammingState.waiting_for_theory_level)  # Устанавливаем состояние ожидания уровня теории
    elif message.text == "Практика":
        await message.answer("Практика для выбранного языка пока недоступна.")
    elif message.text == "Назад":
        await state.clear()
        await command_start_handler(message)

# Обработка выбора уровня теории
@dp.message(ProgrammingState.waiting_for_theory_level)
async def handle_theory_level_selection(message: Message, state: FSMContext) -> None:
    if message.text == "1 уровень - Базовые конструкции":
        await message.answer("Теория для 1 уровня: Базовые конструкции Python.")
    elif message.text == "2 уровень - Модули (встроенные в Python)":
        await message.answer("Теория для 2 уровня: Модули в Python.")
    elif message.text == "3 уровень - Углубление в базовые конструкции":
        await message.answer("Теория для 3 уровня: Углубление в базовые конструкции Python.")
    elif message.text == "Назад":
        await state.set_state(ProgrammingState.waiting_for_section)  # Возвращаемся к выбору раздела
        await handle_language_selection(message, state)

# Запуск бота
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())