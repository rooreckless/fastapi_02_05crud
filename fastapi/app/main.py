from fastapi import FastAPI,HTTPException

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
    # **book.model_dump()はPydanticモデルのインスタンスからのメソッド(bookはBookSchema型 =pydantic.BaseModelを継承したクラスのもの)である。
    # そのインスタンスから辞書形式のデータにアンパック({title=値,category=値}という属性と値でキーバリューの辞書)にしたうえで、
    # さらに新しいidを発行してキーバリューを増やした上で、BookResponseSchemaに入れ直している。
    new_book =BookResponseSchema(id=new_book_id, **book.model_dump())
    # ダミーデータに追加 = さっきのnew_bookをリストに追加する
    books.append(new_book)
    # 登録書籍データを返す
    return new_book

#----書籍のGET用(一覧を返す)ルート--------------------------
@app.get("/books/", response_model=list[BookResponseSchema])
async def read_books():
    # 登録されている全書籍を返す
    return books

#----書籍のGET用(IDを指定)ルート--------------------------
@app.get("/books/{book_id}", response_model=BookResponseSchema)
async def read_book(book_id: int):
    # パスパラメータのみで書籍を取得する
    for book in books:
        if book.id == book_id:
            return book
    # なかった場合は例外を返す
    raise HTTPException(status_code=404, detail="Book not found")

#----書籍のPUT用(IDを指定して更新)ルート--------------------------
@app.put("/books/{book_id}", response_model=BookResponseSchema)
async def update_book(book_id: int,book: BookSchema):
    # パスパラメータ{book_id}とリクエストボディBookSchemaの両方を使っている
    for index, existing_book in enumerate(books):
        if existing_book.id == book_id:
            # パスパラメータのidと一致するダミーデータがあった場合
            # postの時と同じように、リクエストボディのbookを{title=値,category=値}という辞書にアンパックし、(book.model_dump()で)
            # さらにid=book_idのキーバリューも追加してBookResponseSchemaに入れ直す = 「既存の本を更新」ということ。
            updated_book = BookResponseSchema(id=book_id, **book.model_dump())
            #更新した本をダミーデータのリストに詰め直す
            books[index] = updated_book
            # 更新した本を返す(BookResponseSchema型だから、idがある状態で帰っている)
            return updated_book
    # なかった場合は例外を返す
    raise HTTPException(status_code=404, detail="Book not found")


#----書籍のDLETE用(IDを指定して削除)ルート--------------------------
# 削除した本の情報をBookResponseSchemaの形式で解す
@app.delete("/books/{book_id}", response_model=BookResponseSchema)
def delete_book(book_id:int):
    #パスパラメータのみで削除を実行する = 以下のforとifはgetの時にかなり近い
    for index, book in enumerate(books):
        if book.id == book_id:
            #ダミーデータのリストから、要素を除去 = pop
            books.pop(index)
            # 削除した本の情報を返す(違和感あるけど)
            return book
    # なかった場合は例外を返す
    raise HTTPException(status_code=404, detail="Book not found")