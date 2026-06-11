# Сайт для теста "Кто ты из фей Winx?"

Сайт создан для прохождения теста "Кто ты из фей Winx?".
Сайт позволяет пользователям пройти тест состоящий из 9
вопросов, узнать с какой феей он больше всего
ассоциируется и получить сертификат о прохождении.

## Основные функции

- **Регистрации имени** - ввод имени пользователя на главное странице для дальнейшего его отображения в финале
  тестирования и для отображения на сертификате
- **Вопросы** - 9 разнообразных вопросов, каждый из которых раскрывает свою сторону личности человека
- **Сертификат** - красочный сертификат о прохождении теста, в котором прописывается: имя пользователя, результат теста,
  номер сертификата, дата прохождения и QR код подтверждения прохождения

## Архитектура проекта

```
test_winx/
├── configs/
│   └── config.ini              # Конфигурационные параметры
├── errors/                     # Ошибки работы приложения
├── logs/                       # Логи приложения
├── static/
│    └── certificate_templates/ # Шаблоны сертификата
│    └── certificates/          # Сертификаты пользователей
│    └── css/                   # Оформление и внешний вид веб-страниц
│        └── fonts/             # Шрифты для текста
│    └── media/
│        └── another/           # Папка для старых медиа файлов
│        └── fairy/             # Картинки с феями для страницы с результатом
│        └── qr_cods/           # QR коды для сертификатов пользователей
│        └── question_pics/     # Картинки для каждого вопроса
│        └── wallpapers/        # Обои для веб-страниц
├── templates/                  # Разметки веб-страниц
├── app.py                      # Основной файл сайта
├── certificates.py             # Создание сертификатов
├── configs.py                  # Конфигурационные переменные
├── databases.py                # Работа с PostgreSQL
├── errors.py                   # Запись ошибок в файл ошибок
├── logs.py                     # Настройка логирования
├── questions.py                # Храниениие вопросов как словарей
```

## Требования

### Системные требования

- Python 3.12+
- PostgreSQL 17+

### Python зависимости

```
Flask
psycopg
Pillow
configparser
```

## Установка и настройка

### 1. Клонирование и настройка окружения

```bash
git clone <repository-url>
cd test_winx
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка базы данных PostgreSQL

Создайте базу данных и выполните SQL скрипт:

```sql
-- Создание таблицы вопросов
CREATE TABLE IF NOT EXISTS public.questions
(
    question_id integer NOT NULL,
    question_text text COLLATE pg_catalog."default",
    fairy_answer jsonb,
    CONSTRAINT questions_pkey PRIMARY KEY (question_id)
);

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS public.users
(
    user_ip inet NOT NULL,
    blum integer,
    stella integer,
    flora integer,
    muza integer,
    tekna integer,
    leyla integer,
    user_name text COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (user_ip)
);

-- Создание таблицы сертификатов
CREATE TABLE IF NOT EXISTS public.certificates
(
    certificate_id text COLLATE pg_catalog."default" NOT NULL,
    user_name text COLLATE pg_catalog."default",
    fairy_result text COLLATE pg_catalog."default",
    date timestamp without time zone,
    CONSTRAINT certificates_pkey PRIMARY KEY (certificate_id)
);

-- Создание таблицы результатов теста
CREATE TABLE IF NOT EXISTS public.winx_results
(
    fairy_name text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    fairy_name_rus text COLLATE pg_catalog."default",
    CONSTRAINT winx_results_pkey PRIMARY KEY (fairy_name)
);
```

### 4. Настройка конфигурации

Создайте файл `configs/config.ini`:

```ini
[sql]

database_name = test_winks_site
user = ваш_пользователь
password = ваш_пароль
host = 127.0.0.1
port = 5432

[web]

host = 127.0.0.1
port = 8080
debug = True

[dir_and_file]

log_dir = logs
log_file = file.log
error_dir = errors
error_file = full_error.doc
certificates_dir = certificates
certificate_templates = certificate_templates
certificate_base = certificate_base.png

[admin]
max_count_question = 8

[text_for_certificate]

user_name_text_size = 172
main_text_size = 128
date_text_size = 72
main_text = Спасибо за прохождение
    нашего теста!
fairy_text = По итогам теста,
    ты фея
date_text = Дата прохождения теста:
serial_number_text = Номер сертификата:
```

### 5. Подготовка ресурсов

- Разместите изображения в папке `static/media/`
- Добавьте шрифты в папку `static/css/fonts/`
- В модуле `databases.py` уберите комментарий со строчки **58**. Один раз запустите модуль,
  чтобы функция заполнила базу данных с вопросами. Как только таблица заполнится вопросами, можете
  обратно закомментировать строчку **58**.

## Запуск сайта

```bash
python app.py
```

Сервер автоматически:

- Настроит логирование
- Подключиться к базе данных

## Логирование

Сервер ведет подробное логирование:

- Уровень логирования настраивается в `configs.py`
- Логи сохраняются в папку `logs/`
- Автоматический ротаций логов

## Поиск и устранение неисправностей

### Распространенные проблемы

1. **Ошибки с изображениями**

- Проверьте наличие файлов изображений
- Проверьте правильность расширений файлов
- Убедитесь в правильности путей

2. **Проблемы с базой данных**

- Проверьте подключение к PostgreSQL
- Убедитесь в правильности SQL скрипта
