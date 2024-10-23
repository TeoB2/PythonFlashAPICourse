from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, publish_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3) #validazione del campo con lunghezza minima e massima
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5) #validazione del campo con range di valori
    publish_date: int = Field(ge=1000, le=9999)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Matteo",
                "description": "Test description",
                "rating": 5,
                "publish_date": 2024
            }
        }
    }

BOOKS = [
    Book(1, 'Title 1', 'Author One', 'Description One', 4, 2012),
    Book(2, 'Title Two', 'Author Two', 'Description Two', 3, 2024),
    Book(3, 'Title Three', 'Author One', 'Description Three', 5, 2019),
    Book(4, 'Title Four', 'Author Four', 'Description Four', 2, 2021),
    Book(5, 'Title Five', 'Author Five', 'Description Five', 1, 2020),
    Book(6, 'Title Six', 'Author Two', 'Description Six', 4, 2018),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int = Query(gt=0, le=5)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    
    return books_to_return

@app.post("/create-books", status_code=status.HTTP_201_CREATED)
async def create_books(book_request: BookRequest):
    new_book = Book(**book_request.model_dump()) #converte in un dizionario
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0) ):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/publish_date/{publish_date}", status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(publish_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == publish_date:
            books_to_return.append(book)
    
    return books_to_return