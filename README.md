# Образовательная платформа на Django

Этот проект представляет собой образовательную платформу, разработанную на Django. Он полностью контейнеризирован с помощью Docker и настроен для автоматического тестирования и развертывания (CI/CD) через GitHub Actions.

## 🚀 Технологии и ключевые особенности

- **Бэкенд:** Django, Django Rest Framework
- **База данных:** PostgreSQL
- **Асинхронные задачи:** Celery, Redis, Celery Beat
- **Веб-сервер:** Nginx + Gunicorn
- **Контейнеризация:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Платежи:** Интеграция со Stripe
- **Аутентификация:** JWT (djangorestframework-simplejwt)
- **Документация API:** drf-yasg (Swagger)
- **Управление зависимостями:** Poetry

---

## ⚙️ Локальная разработка

### 1. Предварительные требования

- Установленный [Docker](https://www.docker.com/products/docker-desktop/)
- Установленный `docker-compose` (обычно поставляется с Docker Desktop)

### 2. Настройка окружения

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <URL_вашего_репозитория>
    cd pythonproject5
    ```

2.  **Создайте файл переменных окружения:**
    Скопируйте шаблон `.env.template` в новый файл `.env`.
    ```bash
    cp .env.template .env
    ```

3.  **Заполните `.env` файл:**
    Откройте файл `.env` и заполните его. Для локального запуска ключевые значения должны быть такими:
    ```ini
    # Настройки PostgreSQL
    POSTGRES_DB=your_db_name
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    DB_HOST=db # <-- Указывает на сервис 'db' в docker-compose.yaml
    DB_PORT=5432

    # Настройки Redis
    REDIS_HOST=redis # <-- Указывает на сервис 'redis' в docker-compose.yaml
    REDIS_PORT=6379

    # Секретный ключ Django
    SECRET_KEY=your_local_secret_key # <-- Любая строка для локального запуска

    # Ключ API для Stripe (необязательно для локального запуска без проверки платежей)
    STRIPE_API_KEY=your_stripe_api_key
    ```

### 3. Запуск проекта

Выполните одну команду для сборки образов и запуска всех контейнеров в фоновом режиме:
```bash
docker-compose up --build -d
```

### 4. Доступ к приложению

- **Веб-приложение:** [http://localhost](http://localhost)
- **API документация (Swagger):** [http://localhost/swagger/](http://localhost/swagger/)

### 5. Полезные команды Docker

- **Просмотр логов** (например, для Django-приложения):
  ```bash
  docker-compose logs -f app
  ```
- **Остановка всех сервисов:**
  ```bash
  docker-compose down
  ```
- **Выполнение `manage.py` команд** (например, создание суперпользователя):
  ```bash
  docker-compose exec app python manage.py createsuperuser
  ```

---

## 📦 Управление зависимостями (Poetry)

Проект использует [Poetry](https://python-poetry.org/) для управления зависимостями.

- **Добавление новой зависимости:**
  ```bash
  poetry add <имя-пакета>
  ```
- **Обновление lock-файла:**
  После изменения `pyproject.toml` или для обновления версий пакетов выполните:
  ```bash
  poetry lock
  ```
  > **Важно:** После этих команд не забудьте закоммитить изменения в файлах `pyproject.toml` и `poetry.lock`.

---

## 🚀 CI/CD и Автоматический деплой

Проект использует GitHub Actions для автоматического тестирования и развертывания на продакшен-сервер.

### 1. Логика работы

- **На Pull Request в ветку `develop`:**
  Запускаются задачи для проверки качества кода:
  1.  `lint`: Проверка стиля кода с помощью `flake8`.
  2.  `test`: Запуск тестов с использованием `pytest`.
  3.  `docker-build-check`: Проверка того, что Docker-образы успешно собираются.

- **При Push (слиянии) в ветку `develop`:**
  Выполняются все те же проверки, и в случае их успеха запускается автоматический деплой:
  1.  `build-and-push`: Собираются и тегируются два Docker-образа (`app` и `nginx`) и отправляются в Docker Hub.
  2.  `deploy`: GitHub Actions подключается к вашему серверу по SSH, скачивает новые образы и перезапускает контейнеры с обновленным кодом.

### 2. Настройка для автоматического деплоя

Для работы деплоя необходимо настроить "секреты" в вашем репозитории на GitHub.

Перейдите в **Settings -> Secrets and variables -> Actions** и создайте следующие секреты:

- `DOCKER_HUB_USERNAME`: Ваш логин на Docker Hub.
- `DOCKER_HUB_ACCESS_TOKEN`: Токен доступа от Docker Hub с правами на чтение и запись.
- `SERVER_IP`: IP-адрес вашего продакшен-сервера.
- `SSH_USER`: Имя пользователя для подключения к серверу по SSH (например, `root` или `ubuntu`).
- `SSH_KEY`: **Приватный** SSH-ключ для доступа к серверу (содержимое файла `~/.ssh/id_rsa`).
- `SECRET_KEY`: Надежный и длинный **продакшен**-ключ для Django.
- `DEPLOY_DIR`: Абсолютный путь к папке проекта на сервере (например, `/home/ubuntu/pythonproject5`).
- `PRODUCTION_ENV_FILE`: Полное содержимое `.env` файла для сервера. Сюда нужно вписать все переменные, включая пароли от базы данных, ключи Stripe и т.д.

### 3. Адрес развернутого приложения

После успешного деплоя приложение будет доступно по адресу: `http://ВАШ_SERVER_IP`