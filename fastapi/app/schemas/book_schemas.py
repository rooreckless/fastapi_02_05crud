# 書籍のデータ構造を定義するスキーマを踏みます

from pydantic import BaseModel

# 書籍の作成と更新に使うスキーマ
class BookSchema(BaseModel):
    # タイトル
    title: str
    # カテゴリ
    category: str

# レスポンス用のスキーマ
# 書籍スキーマを継承してidを含める
class BookResponseSchema(BookSchema):
    # ID
    id: int