# Email:Pass AntiPublic Telegram Bot

Это простой бот для Telegram, написанный на языке Python, который позволяет проверить базы данных на уникальность.

## Требования

Прежде чем начать использование этого скрипта, убедитесь, что у вас установлены следующие компоненты:

- Python версии 3.6 и выше
- Библиотеки из requirements.txt (`pip install requirements.txt`)

## Установка

1. Склонируйте репозиторий или загрузите файлы `main.py` на свой компьютер.
2. Установите необходимые зависимости.
3. Наслаждайтесь ботом.

## Конфигурация

Перед запуском скрипта необходимо сконфигурировать некоторые параметры.

1. Откройте файл `main.py` и настройте следующие параметры:
   - `TOKEN` - токен вашего бота Telegram. Вы можете получить его, создав нового бота с помощью @BotFather в Telegram.
   - `DB_PATH` - путь к базе данных sqlite3. Укажите полный путь к файлу базы данных, а лучше оставьте как есть (база создастся автоматически).
   
2. Сохраните изменения в файле `main.py`.

## Запуск

1. Откройте терминал и перейдите в папку с проектом.
2. Запустите скрипт, выполнив следующую команду: `python main.py`.
3. Ваш бот теперь работает! Вы можете найти его в Telegram и начать использовать его, отправив сообщение или команду.

## Использование

Ваш бот реагирует на команды и сообщения, которые вы отправляете ему в Telegram. Вот список доступных команд:

- `/start` - Запустить бота и отобразить приветственное сообщение.
- `<email>:<password>` - Проверить строку с почтой и паролем. Замените `<email>` и `<password>` на соответствующие значения.
- `<file>.txt` - Проверить файл с почтами и паролями. Просто отправьте текстовый документ для старта проверки.

## Примечания

- База данных AntiPublic содержит учетные записи, скомпрометированные в результате хакерских атак
