# 書籍のデータ構造を定義するスキーマを踏みます

from pydantic import BaseModel,Field

# 書籍の作成と更新に使うスキーマ
class BookSchema(BaseModel):
    # タイトル
    title: str
    # カテゴリ
    category: str
    # 値段
    price: float = Field(..., gt=0,le=5000,)

# レスポンス用のスキーマ
# 書籍スキーマを継承してidを含める
class BookResponseSchema(BookSchema):
    # ID
    id: int