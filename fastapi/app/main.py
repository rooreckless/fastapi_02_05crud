from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI + PostgreSQL + Docker Compose!"}



#----書籍のPOST用ルート--------------------------
# デモ用のデータベース代わりに使うリスト
from .schemas.book_schemas import BookSchema, BookResponseSchema
# ダミーの書籍リスト
books: list[BookResponseSchema]=[
    BookResponseSchema(id=1, title="Python入門", category="technical"),
    BookResponseSchema(id=2, title="初めてのプログラミング", category="technical"),
    BookResponseSchema(id=3, title="進む巨人", category="comics"),
    BookResponseSchema(id=4, title="DBおやじ", category="comics"),
    BookResponseSchema(id=5, title="週間ダイヤモンド", category="magazine"),
    BookResponseSchema(id=6, title="ザ・社長", category="magazine"),
]


@app.post("/books/", response_model=BookResponseSchema) #<- response_modelがレスポンス用スキーマを指す
async def create_book(book: BookSchema):                #<- 引数bookはpostリクエスト用スキーマ型を指定   
    # new_book = BookResponseSchema(id=len(books) + 1, **book.dict())
    # 新しい書籍IDを作成
    new_book_id = max([book.id for book in books],default=0)+1
    # 新しい書籍を作成
    new_book =BookResponseSchema(id=new_book_id, **book.model_dump())
    # ダミーデータに追加
    books.append(new_book)
    # 登録書籍データを返す
    return new_book

#----書籍のGET用(一覧を返す)ルート--------------------------
@app.get("/books/", response_model=list[BookResponseSchema])
async def read_books():
    # 登録されている全書籍を返す
    return books