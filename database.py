# import psycopg2
# from psycopg2 import sql

# # Подключение к базе данных
# def get_db_connection():
#     conn = psycopg2.connect(
#         dbname="telegram_bot",  # Имя базы данных
#         user="bot_user",       # Имя пользователя
#         password="your_password",  # Пароль
#         host="localhost",      # Хост (обычно localhost)
#         port="5432"            # Порт (по умолчанию 5432)
#     )
#     return conn

# # Инициализация базы данных
# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Создание таблиц
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS days (
#             id SERIAL PRIMARY KEY,
#             name TEXT NOT NULL
#         )
#     ''')

#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS slots (
#             id SERIAL PRIMARY KEY,
#             day_id INTEGER REFERENCES days(id),
#             time TEXT NOT NULL,
#             is_booked BOOLEAN DEFAULT FALSE
#         )
#     ''')

#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS bookings (
#             id SERIAL PRIMARY KEY,
#             slot_id INTEGER REFERENCES slots(id),
#             user_id INTEGER,
#             user_name TEXT
#         )
#     ''')

#     # Заполнение дней и слотов (если они еще не созданы)
#     days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
#     time_slots = [f"{hour}:00-{hour+1}:00" for hour in range(15, 22)]

#     for day_name in days:
#         cursor.execute('INSERT INTO days (name) VALUES (%s) ON CONFLICT (name) DO NOTHING', (day_name,))

#     for day_id in range(1, 8):
#         for time_slot in time_slots:
#             cursor.execute('INSERT INTO slots (day_id, time) VALUES (%s, %s) ON CONFLICT (day_id, time) DO NOTHING', (day_id, time_slot))

#     conn.commit()
#     conn.close()

# # Получение доступных слотов
# def get_available_slots(day_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM slots WHERE day_id = %s AND is_booked = FALSE', (day_id,))
#     slots = cursor.fetchall()
#     conn.close()
#     return slots

# # Бронирование слота
# def book_slot(slot_id, user_id, user_name):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('UPDATE slots SET is_booked = TRUE WHERE id = %s', (slot_id,))
#     cursor.execute('INSERT INTO bookings (slot_id, user_id, user_name) VALUES (%s, %s, %s)', (slot_id, user_id, user_name))
#     conn.commit()
#     conn.close()

# # Получение всех бронирований
# def get_all_bookings():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT days.name, slots.time, bookings.user_name 
#         FROM bookings
#         JOIN slots ON bookings.slot_id = slots.id
#         JOIN days ON slots.day_id = days.id
#     ''')
#     bookings = cursor.fetchall()
#     conn.close()
#     return bookings