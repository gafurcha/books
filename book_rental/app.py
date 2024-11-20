# app.py
from flask import Flask, request, jsonify
from models import db, Book
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

swagger = Swagger(app)

with app.app_context():
    db.create_all()  # Создание таблиц

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

# Эндпоинт для чтения конкретной книги (GET /api/books/<id>)
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    """Чтение конкретной книги
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Информация о книге
      404:
        description: Книга не найдена
    """
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'available': book.available})

# Эндпоинт для чтения всех книг (GET /api/books)
@app.route('/api/books', methods=['GET'])
def get_all_books():
    """Чтение всех книг
    ---
    responses:
      200:
        description: Список всех книг
    """
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'available': book.available} for book in books])

# Эндпоинт для обновления книги (PUT /api/books/<id>)
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    """Обновление книги
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
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
      200:
        description: Книга обновлена
      404:
        description: Книга не найдена
    """
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    data = request.json
    book.title = data['title']
    book.author = data['author']
    book.available = data['available']
    db.session.commit()
    return jsonify({'message': 'Book updated'})

# Эндпоинт для удаления книги (DELETE /api/books/<id>)
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    """Удаление книги
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Книга удалена
      404:
        description: Книга не найдена
    """
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})


if __name__ == '__main__':
    app.run(debug=True)
