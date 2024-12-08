from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)

DATABASE = 'library.db'
TOKEN = 'hghjdsagshdgajahgdajhgdjhsk'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_first_request
def initialize_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        # Create books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                published_year INTEGER
            )
        ''')
        # Create members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')

@app.before_request
def authenticate():
    token = request.headers.get('Authorization')
    if not token or token != f"Bearer {TOKEN}":
        abort(401, description="Unauthorized")

@app.route('/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'GET':
        title = request.args.get('title')
        author = request.args.get('author')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        query = "SELECT * FROM books WHERE 1=1"
        params = []
        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")
        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")
        query += " LIMIT ? OFFSET ?"
        params.extend([per_page, (page - 1) * per_page])
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            books = cursor.fetchall()
        return jsonify(books)

    elif request.method == 'POST':
        data = request.json
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO books (title, author, published_year) VALUES (?, ?, ?)',
                           (data['title'], data['author'], data['published_year']))
            conn.commit()
        return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books/<int:book_id>', methods=['PUT', 'DELETE'])
def modify_book(book_id):
    if request.method == 'PUT':
        data = request.json
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE books SET title = ?, author = ?, published_year = ? WHERE id = ?',
                           (data['title'], data['author'], data['published_year'], book_id))
            conn.commit()
        return jsonify({'message': 'Book updated successfully'})

    elif request.method == 'DELETE':
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
        return jsonify({'message': 'Book deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
