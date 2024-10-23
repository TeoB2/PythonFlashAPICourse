from fastapi import Body, FastAPI
from typing import List, Optional

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author One', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/api-endpoint")
async def first_api():
    return {"message": "Hello World"}

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/book/{book_title}")
async def read_book_title(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book
        
@app.get("/book/")
async def read_book_category(book_category: Optional[str] = None):
    if book_category:
        book_finds = []
        for book in BOOKS:
            if book.get('category').casefold() == book_category.casefold():
                book_finds.append(book)
        return book_finds
    return {"message": "Please provide a book category"}

@app.get("/books/{book_author}")
async def read_book_category(book_author: str, book_category: Optional[str] = None):
    if book_author:
        book_finds = []
        for book in BOOKS:
            if book.get('author').casefold() == book_author.casefold():
                if book_category is None or book.get('category').casefold() == book_category.casefold():
                    book_finds.append(book)
        return book_finds
    return {"message": "Please provide a book category"}

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == updated_book['title'].casefold():
            BOOKS[i] = updated_book
            return {"message": "Book updated successfully"}
        
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == book_title.casefold():
            del BOOKS[i]
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}

@app.post("/books/get_author_books")
async def get_author_books(author_name: str):
    author_books = []
    for book in BOOKS:
        if book['author'].casefold() == author_name.casefold():
            author_books.append(book)
    if len(author_books) == 0:
        return {"message": "Author not found"}
    else:
        return author_books