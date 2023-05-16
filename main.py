import sqlite3
import io
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType
import re
import os

directory = 'documents'  # путь к директории, в которой нужно удалить файлы

# Рекурсивно обходит все поддиректории и удаляет файлы
for root, dirs, files in os.walk(directory):
  for file in files:
    os.remove(os.path.join(root, file))

# Токен бота
TOKEN = 'СЮДАТОКЕН'

# Путь до базы данных
DB_PATH = "antipublic.db"

# SQL-запрос для создания таблицы
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS data (
    email TEXT,
    password TEXT
)
"""


# Функция для создания базы данных и таблицы
def create_database():
  # Подключаемся к базе данных
  conn = sqlite3.connect(DB_PATH)
  # Создаем таблицу, если ее нет
  conn.execute(CREATE_TABLE_QUERY)
  # Закрываем соединение
  conn.close()


# Создаем базу данных
create_database()

# Создаем экземпляр бота
bot = Bot(token=TOKEN)

# Создаем диспетчер для обработки сообщений
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Обрабатываем команду /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
  # Отвечаем на команду
  await message.answer(
    "👋 Привет! Я бот для работы с базой данных\n"
    "💌 Отправь мне свой email и пароль, разделив их символом ':'\n"
    "📁 Если нужно добавить несколько строк сразу, просто отправь их мне"
    "📄 Также я могу принимать текстовые документы до 20Мб (ограничение Telegram)"
  )


# Обрабатываем текстовые сообщения и документы
@dp.message_handler(content_types=[ContentType.TEXT, ContentType.DOCUMENT])
async def handle_message(message: types.Message):
  # Определяем тип контента
  content_type = message.content_type

  # Если получено текстовое сообщение
  if content_type == ContentType.TEXT:
    # Разделяем текст сообщения на отдельные строки
    lines = message.text.split("\n")
  # Если получен документ
  elif content_type == ContentType.DOCUMENT:
    # Получаем информацию о документе
    document = message.document
    file_name = document.file_name

    # Проверяем, является ли файл текстовым
    if file_name.endswith(".txt"):
      # Скачиваем файл
      result = await message.document.download()
      file_name = result.name

      # Открываем файл и разделяем его содержимое на отдельные строки
      with open(file_name, "r") as f:
        lines = f.readlines()
        f.close()

    else:
      # Если файл не является текстовым, отвечаем пользователю
      await message.answer(
        "❌ Извините, но я умею обрабатывать только текстовые файлы.")
      return

  # Подключаемся к базе данных
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  # Добавляем записи в таблицу
  unique_lines = set()
  for line in lines:
    email, _, password = line.partition(":")
    # Проверяем, есть ли уже такая запись в базе данных
    count = conn.execute(
      "SELECT COUNT(*) FROM data WHERE email = ? AND password = ?",
      (email.strip(), password.strip())).fetchone()[0]
    if count == 0:
      # Проверяем, являются ли данные правильными
      if not re.match(r"[^@]+@[^@]+\.[^@]+:[^:]+", line):
        continue
      # Добавляем уникальные записи в список
      cursor.execute('INSERT INTO data VALUES (?, ?)',
                     (email.strip(), password.strip()))
      unique_lines.add(line.strip())
  # Сохраняем изменения
  conn.commit()
  # Закрываем соединение
  conn.close()
  # Получаем количество уникальных записей в базе данных
  count = len(unique_lines)
  # Отправляем список строк в виде текстового документа
  if count > 0:
    await message.answer_document(
      types.InputFile(io.BytesIO("\n".join(unique_lines).encode()),
                      filename="unique_lines.txt"),
      caption=
      f"📝 Обработано {len(lines)} записей\n💫 Уникальных записей: {count}")
  else:
    await message.answer("Нет уникальных записей 😢")


# Запускаем бота
if __name__ == "__main__":
  from aiogram import executor
  executor.start_polling(dp, skip_updates=True)
