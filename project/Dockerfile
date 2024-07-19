# Используем официальный образ Python в качестве базового образа
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы проекта в рабочую директорию
COPY . /app/

# Выполняем миграции
RUN python manage.py migrate

# Открываем порт 8000 для доступа
EXPOSE 8000

# Устанавливаем команду по умолчанию для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]