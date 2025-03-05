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
API_TOKEN = '8095908870:AAHeTDeiL6L9xujI53oVZULu-SYZjoWTEbI'  # Замените на ваш токен
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
                "💬 Описание из кодификатора: Умение представлять и считывать данные в разных типах информационных моделей (схемы, карты, таблицы, графики и формулы)\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)
            
        if task_number == 2:
            info = (
                "💬 Описание из кодификатора: Умение строить таблицы истинности и логические схемы\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)

        if task_number == 3:
            info = (
                "💬 Описание из кодификатора: Умение поиска информации в реляционных базах данных\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Да\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)
        if task_number == 4:
            info = (
                "💬 Описание из кодификатора: Умение кодировать и декодировать информацию\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 2"
            )
            await message.answer(info)
        if task_number == 5:
            info = (
                "💬 Описание из кодификатора: Формальное исполнение простого алгоритма, записанного на естественном языке, или умение создавать линейный алгоритм для формального исполнителя с ограниченным набором команд, или умение восстанавливать исходные данные линейного алгоритма по результатам его работы\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 4"
            )
            await message.answer(info)
        if task_number == 6:
            info = (
                "💬 Описание из кодификатора: Определение возможных результатов работы простейших алгоритмов управления исполнителями и вычислительных алгоритмов\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 4"
            )
            await message.answer(info)
        if task_number == 7:
            info = (
                "💬 Описание из кодификатора: Умение определять объём памяти, необходимый для хранения графической и звуковой информации\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 5"
            )
            await message.answer(info)
        
        if task_number == 8:
            info = (
                "💬 Описание из кодификатора: Знание основных понятий и методов, используемых при измерении количества информации\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 4"
            )
            await message.answer(info)
        if task_number == 9:
            info = (
                "💬 Описание из кодификатора: Умение обрабатывать числовую информацию в электронных таблицах\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Да\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 6"
            )
            await message.answer(info)
        if task_number == 10:
            info = (
                "💬 Описание из кодификатора: Информационный поиск средствами текстового процессора\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Да\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)
        if task_number == 11:
            info = (
                "💬 Описание из кодификатора: Информационный поиск средствами текстового процессора\n"
                "⚔️ Уровень сложности задания: Базовый\n"
                "💻 Требуется использование специализированного программного обеспечения: Да\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)
        if task_number == 12:
            info = (
                "💬 Описание из кодификатора: Умение исполнить алгоритм для конкретного исполнителя с фиксированным набором команд\n"
                "⚔️ Уровень сложности задания: Продвинутый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 6"
            )
            await message.answer(info)
        if task_number == 13:
            info = (
                "💬 Описание из кодификатора: Умение использовать маску подсети\n"
                "⚔️ Уровень сложности задания: Продвинутый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)
        if task_number == 14:
            info = (
                "💬 Описание из кодификатора: Знание позиционных систем счисления\n"
                "⚔️ Уровень сложности задания: Продвинутый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)
        if task_number == 15:
            info = (
                "💬 Описание из кодификатора: Знание основных понятий и законов математической логики\n"
                "⚔️ Уровень сложности задания: Продвинутый\n"
                "💻 Требуется использование специализированного программного обеспечения: Нет\n"
                "📈 Макс. балл за выполнение задания: 1\n"
                "⌚ Примерное время выполнения задания (мин.): 3"
            )
            await message.answer(info)
        


    elif message.text == "Теория":
        if task_number == 1:
            await message.answer("Теория для задания 1: https://skyteach.ru/informatika/ege-po-informatike-teoriya-grafov/")
        if task_number == 2:
            await message.answer("Теория для задания 2: https://skyteach.ru/informatika/razbor-2-zadaniya-iz-ege-po-informatike-2023/")
        if task_number == 3:
            await message.answer("Теория для задания 3: https://dzen.ru/a/ZJqUVYFawTm8MUXL")
        if task_number == 4:
            await message.answer("Теория для задания 4: https://labs-org.ru/ege-4/")
        if task_number == 5:
            await message.answer("Теория для задания 5: https://labs-org.ru/ege-5/")
        if task_number == 6:
            await message.answer("Теория для задания 6: https://dzen.ru/a/ZDaJmklDKyPi6SJo")
        if task_number == 7:
            await message.answer("Теория для задания 7: https://labs-org.ru/ege-7/")
        if task_number == 8:
            await message.answer("Теория для задания 8: https://labs-org.ru/ege-8/")
        if task_number == 9:
            await message.answer("Теория для задания 9: https://labs-org.ru/ege-9/")
        if task_number == 10:
            await message.answer("Теория для задания 10: https://code-enjoy.ru/ege_po_informatike_2025_zadanie_10_poisk_v_tekste/")
        if task_number == 11:
            await message.answer("Теория для задания 11: https://labs-org.ru/ege-11/")
        if task_number == 12:
            await message.answer("Теория для задания 12: https://egeturbo.ru/ege/inf/tasks/12")
        if task_number == 13:
            await message.answer("Теория для задания 13: https://dzen.ru/a/ZWrNeJBMV1_JtLMC")
        if task_number == 14:
            await message.answer("Теория для задания 14: :https://code-enjoy.ru/ege_po_informatike_2025_zadanie_14_chempionskaya_podgotoka/")
        if task_number == 15:
            await message.answer("Теория для задания 15: https://code-enjoy.ru/ege_po_informatike_2025_zadanie_15_prostim_yazikom/")


    elif message.text == "Практика":
        if task_number == 1:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру 1:\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=1&answers=on&varId=\n\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=7bea7f84-c854-45ed-ac97-17d7bb823723&category_id=1d59eed0-1914-4f79-9771-5fff8feaf01b&category_id=a3b4e9aa-e02f-4182-8243-eb7841e37706&sort_by=newFirst&level=2&source=all\n\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=7bea7f84-c854-45ed-ac97-17d7bb823723&category_id=1d59eed0-1914-4f79-9771-5fff8feaf01b&category_id=a3b4e9aa-e02f-4182-8243-eb7841e37706&sort_by=newFirst&level=4&level=3&source=all\n\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=7bea7f84-c854-45ed-ac97-17d7bb823723&category_id=1d59eed0-1914-4f79-9771-5fff8feaf01b&category_id=a3b4e9aa-e02f-4182-8243-eb7841e37706&sort_by=newFirst&level=5&source=all"
            )
            await message.answer(practice_links)
        if task_number == 2:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру 2\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=2&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=b26ff674-4ab4-4c13-96e7-2db1028581d0&sort_by=newFirst&category_id=bca9a630-12a2-4206-b763-2edd262c40fb&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=b26ff674-4ab4-4c13-96e7-2db1028581d0&sort_by=newFirst&category_id=bca9a630-12a2-4206-b763-2edd262c40fb&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=b26ff674-4ab4-4c13-96e7-2db1028581d0&sort_by=newFirst&category_id=bca9a630-12a2-4206-b763-2edd262c40fb&level=5&source=all"
            )
            await message.answer(practice_links)
        if task_number == 3:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру 3\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=4&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=75a8cd9b-0c85-48b4-8ebe-1e7b0f2dbc86&sort_by=newFirst&category_id=e2cefbce-b757-41c1-ac06-b5932dd1ccd2&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=75a8cd9b-0c85-48b4-8ebe-1e7b0f2dbc86&sort_by=newFirst&category_id=e2cefbce-b757-41c1-ac06-b5932dd1ccd2&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=75a8cd9b-0c85-48b4-8ebe-1e7b0f2dbc86&sort_by=newFirst&category_id=e2cefbce-b757-41c1-ac06-b5932dd1ccd2&level=5&source=all"
            )
            await message.answer(practice_links)           
        if task_number == 4:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n" 
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=8&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "asserthttps://education.yandex.ru/ege/tasks?task_id=3af9869d-b61c-44bb-bbfc-24c9964ca947&sort_by=newFirst&category_id=0aaab24e-f6ae-48e2-8a86-7be41c497513&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=3af9869d-b61c-44bb-bbfc-24c9964ca947&sort_by=newFirst&category_id=0aaab24e-f6ae-48e2-8a86-7be41c497513&level=4&level=3&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=3af9869d-b61c-44bb-bbfc-24c9964ca947&sort_by=newFirst&category_id=0aaab24e-f6ae-48e2-8a86-7be41c497513&level=5&source=all"
            )
            await message.answer(practice_links)  
        if task_number == 5:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=10&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=8dabca53-b71d-46d6-8dc5-458a89e1ea74&sort_by=newFirst&category_id=0b7f324e-1871-4477-87a9-46bbd5406c0f&category_id=a1a4f404-5b80-4189-9701-ef341f7307f0&category_id=37d48d40-d8c3-42de-8b5f-1c5958ff1564&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=8dabca53-b71d-46d6-8dc5-458a89e1ea74&sort_by=newFirst&category_id=0b7f324e-1871-4477-87a9-46bbd5406c0f&category_id=a1a4f404-5b80-4189-9701-ef341f7307f0&category_id=37d48d40-d8c3-42de-8b5f-1c5958ff1564&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=8dabca53-b71d-46d6-8dc5-458a89e1ea74&sort_by=newFirst&category_id=0b7f324e-1871-4477-87a9-46bbd5406c0f&category_id=a1a4f404-5b80-4189-9701-ef341f7307f0&category_id=37d48d40-d8c3-42de-8b5f-1c5958ff1564&level=5&level=4&source=all"
            )
            await message.answer(practice_links)
        if task_number == 6:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=20&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=df0219c9-04a7-4ec7-a1f4-ea6d9920f86b&sort_by=newFirst&category_id=2735658d-0600-43a3-867d-6153c4837895&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=df0219c9-04a7-4ec7-a1f4-ea6d9920f86b&sort_by=newFirst&category_id=2735658d-0600-43a3-867d-6153c4837895&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=df0219c9-04a7-4ec7-a1f4-ea6d9920f86b&sort_by=newFirst&category_id=2735658d-0600-43a3-867d-6153c4837895&level=5&source=all"
            )
            await message.answer(practice_links)
        if task_number == 7:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=40&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=b70557ea-1bee-40bd-a3e8-79949ba7c8a5&sort_by=newFirst&category_id=c740c01d-0de7-4206-af42-a8af027e4790&category_id=3f514947-a547-4857-8b6f-5d810818a72c&category_id=c797527c-bdae-418c-9ccf-d560452b09c2&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=b70557ea-1bee-40bd-a3e8-79949ba7c8a5&sort_by=newFirst&category_id=c740c01d-0de7-4206-af42-a8af027e4790&category_id=3f514947-a547-4857-8b6f-5d810818a72c&category_id=c797527c-bdae-418c-9ccf-d560452b09c2&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=b70557ea-1bee-40bd-a3e8-79949ba7c8a5&sort_by=newFirst&category_id=c740c01d-0de7-4206-af42-a8af027e4790&category_id=3f514947-a547-4857-8b6f-5d810818a72c&category_id=c797527c-bdae-418c-9ccf-d560452b09c2&level=5&source=all"
            )
            await message.answer(practice_links)  
        if task_number == 8:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=80&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=fce0ac94-fb12-47fe-9426-c99181633176&sort_by=newFirst&category_id=9d389c73-5d61-4eeb-8ad1-bb790277cbe1&category_id=17b13a8a-0ad2-4555-a8ad-92b3a7e80ff1&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=fce0ac94-fb12-47fe-9426-c99181633176&sort_by=newFirst&category_id=9d389c73-5d61-4eeb-8ad1-bb790277cbe1&category_id=17b13a8a-0ad2-4555-a8ad-92b3a7e80ff1&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=fce0ac94-fb12-47fe-9426-c99181633176&sort_by=newFirst&category_id=9d389c73-5d61-4eeb-8ad1-bb790277cbe1&category_id=17b13a8a-0ad2-4555-a8ad-92b3a7e80ff1&level=5&source=all"
            )
            await message.answer(practice_links)
        if task_number == 9:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=100&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=1f5c3993-252c-4ed4-9d64-62880fde611c&sort_by=newFirst&category_id=97fe3c2e-a048-4c26-847e-54f50bc1d271&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=1f5c3993-252c-4ed4-9d64-62880fde611c&sort_by=newFirst&category_id=97fe3c2e-a048-4c26-847e-54f50bc1d271&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=1f5c3993-252c-4ed4-9d64-62880fde611c&sort_by=newFirst&category_id=97fe3c2e-a048-4c26-847e-54f50bc1d271&level=5&source=all"                
            )
            await message.answer(practice_links) 
        if task_number == 10:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=200&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=9b1012c3-1831-4a21-b803-e96043aa42c3&sort_by=newFirst&category_id=ecc9f560-c468-43f3-a6eb-9c147c003372&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=9b1012c3-1831-4a21-b803-e96043aa42c3&sort_by=newFirst&category_id=ecc9f560-c468-43f3-a6eb-9c147c003372&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=9b1012c3-1831-4a21-b803-e96043aa42c3&sort_by=newFirst&category_id=ecc9f560-c468-43f3-a6eb-9c147c003372&level=5&source=all"
            )
            await message.answer(practice_links)  
        if task_number == 11:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=400&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=10689f58-86a2-42e2-97fe-df42799b136d&sort_by=newFirst&category_id=25169154-febf-477e-b638-d5b569eab3fc&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=10689f58-86a2-42e2-97fe-df42799b136d&sort_by=newFirst&category_id=25169154-febf-477e-b638-d5b569eab3fc&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=10689f58-86a2-42e2-97fe-df42799b136d&sort_by=newFirst&category_id=25169154-febf-477e-b638-d5b569eab3fc&level=5&source=all"                
            )
            await message.answer(practice_links)
        if task_number == 12:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=800&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=a477ba72-aab7-42a2-99a8-8ee21e665437&sort_by=newFirst&category_id=ed841019-c16f-4523-bbfe-3f445be3da0d&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=a477ba72-aab7-42a2-99a8-8ee21e665437&sort_by=newFirst&category_id=ed841019-c16f-4523-bbfe-3f445be3da0d&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=a477ba72-aab7-42a2-99a8-8ee21e665437&sort_by=newFirst&category_id=ed841019-c16f-4523-bbfe-3f445be3da0d&level=5&source=all"
            )
            await message.answer(practice_links)
        if task_number == 13:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=1000&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=dd0c814a-4751-46b6-8cdd-abe8b0faaf60&sort_by=newFirst&category_id=d553da2b-36f5-469d-b340-27ed4e17aff6&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=dd0c814a-4751-46b6-8cdd-abe8b0faaf60&sort_by=newFirst&category_id=d553da2b-36f5-469d-b340-27ed4e17aff6&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=dd0c814a-4751-46b6-8cdd-abe8b0faaf60&sort_by=newFirst&category_id=d553da2b-36f5-469d-b340-27ed4e17aff6&level=5&source=all"                
            )
            await message.answer(practice_links)  
        if task_number == 14:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=2000&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=80bfe036-c91a-441b-920f-ea118c7f9bfc&sort_by=newFirst&category_id=addca5d5-e72e-4201-aeab-51f97d14f397&category_id=796d4184-4c3a-4eb0-bb66-933f69eca3aa&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=80bfe036-c91a-441b-920f-ea118c7f9bfc&sort_by=newFirst&category_id=addca5d5-e72e-4201-aeab-51f97d14f397&category_id=796d4184-4c3a-4eb0-bb66-933f69eca3aa&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=80bfe036-c91a-441b-920f-ea118c7f9bfc&sort_by=newFirst&category_id=addca5d5-e72e-4201-aeab-51f97d14f397&category_id=796d4184-4c3a-4eb0-bb66-933f69eca3aa&level=5&source=all"                
            )
            await message.answer(practice_links)
        if task_number == 15:
            practice_links = (
                "🚀 Сайт Полякова, генератор по номеру\n"
                "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewVar&select=4000&answers=on&varId=\n"
                "🥳 Легче ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=26ec6e20-908f-47c2-b415-20873e9136e4&sort_by=newFirst&category_id=c5930d96-d5f5-43ea-ac06-8c02ef86ada6&category_id=afc5a82b-98b3-4139-ba75-389bd73f4a2b&category_id=abeb5530-0db0-4d23-aa03-b966638c9a92&category_id=123053b3-fa0d-49b7-be13-8823c3e4c22e&category_id=80962457-270f-4d7c-a7e6-430ad6a3f3c2&category_id=8a0e070f-d023-4d5b-b253-548c27223561&level=1&level=2&source=all\n"
                "✅ Уровень ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=26ec6e20-908f-47c2-b415-20873e9136e4&sort_by=newFirst&category_id=c5930d96-d5f5-43ea-ac06-8c02ef86ada6&category_id=afc5a82b-98b3-4139-ba75-389bd73f4a2b&category_id=abeb5530-0db0-4d23-aa03-b966638c9a92&category_id=123053b3-fa0d-49b7-be13-8823c3e4c22e&category_id=80962457-270f-4d7c-a7e6-430ad6a3f3c2&category_id=8a0e070f-d023-4d5b-b253-548c27223561&level=3&level=4&source=all\n"
                "💀 Сложнее ЕГЭ\n"
                "https://education.yandex.ru/ege/tasks?task_id=26ec6e20-908f-47c2-b415-20873e9136e4&sort_by=newFirst&category_id=c5930d96-d5f5-43ea-ac06-8c02ef86ada6&category_id=afc5a82b-98b3-4139-ba75-389bd73f4a2b&category_id=abeb5530-0db0-4d23-aa03-b966638c9a92&category_id=123053b3-fa0d-49b7-be13-8823c3e4c22e&category_id=80962457-270f-4d7c-a7e6-430ad6a3f3c2&category_id=8a0e070f-d023-4d5b-b253-548c27223561&level=5&source=all"
            )
            await message.answer(practice_links)

            
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