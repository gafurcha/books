## Описание проекта

Данный проект реализует REST API для информационной системы пункта проката книг. API позволяет выполнять основные операции CRUD (Создание, Чтение, Обновление, Удаление) с ресурсом "Книга".

## Эндпоинты API

API включает следующие ключевые эндпоинты:

1. Создание книги
   - Метод: POST
   - Эндпоинт: /api/books
   - Описание: Создает новую книгу в системе.
   - Запрос:
     
     {
       "title": "Название книги",
       "author": "Имя автора",
       "available": true
     }
     
   - Ответ:
     - 201: Книга успешно создана.

2. Получить информацию о книге
   - Метод: GET
   - Эндпоинт: /api/books/<id>
   - Описание: Получает информацию о книге по её идентификатору.
   - Ответ:
     - 200: Информация о книге.
     - 404: Книга не найдена.

3. Получить список всех книг
   - Метод: GET
   - Эндпоинт: /api/books
   - Описание: Возвращает список всех доступных книг.
   - Ответ:
     - 200: Список книг.

4. Обновление книги
   - Метод: PUT
   - Эндпоинт: /api/books/<id>
   - Описание: Обновляет информацию о книге по её идентификатору.
   - Запрос:
     
     {
       "title": "Новое название книги",
       "author": "Новое имя автора",
       "available": false
     }
     
   - Ответ:
     - 200: Книга успешно обновлена.
     - 404: Книга не найдена.

5. Удаление книги
   - Метод: DELETE
   - Эндпоинт: /api/books/<id>
   - Описание: Удаляет книгу по её идентификатору.
   - Ответ:
     - 200: Книга успешно удалена.
     - 404: Книга не найдена.

## Установка

### Шаг 1: Установите необходимые зависимости

Убедитесь, что у вас установлен пакетный менеджер pip. Используйте следующий команды для установки необходимых библиотек:

pip install Flask Flasgger Flask-SQLAlchemy


### Шаг 2: Создание и настройка приложения

Создайте файл app.py и вставьте следующий код:

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
swagger = Swagger(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)

with app.app_context():
    db.create_all()  # Создание таблиц

# Эндпоинты...

# Эндпоинт для создания книги (POST /api/books)
@app.route('/api/books', methods=['POST'])
def create_book():
    """Создание книги
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
            available:
              type: boolean
    responses:
      201:
        description: Книга создана
      400:
        description: Ошибка в данных
    """
    data = request.json
    new_book = Book(title=data['title'], author=data['author'], available=data['available'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'id': new_book.id}), 201

# Остальные эндпоинты...

if __name__ == '__main__':
    app.run(debug=True)


### Шаг 3: Запуск приложения

Запустите приложение, выполнив следующую команду в терминале:

python app.py


### Шаг 4: Просмотр документации Swagger

Откройте браузер и перейдите по адресу http://localhost:5000/apidocs/ для просмотра документации вашего API.
