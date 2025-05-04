from flask import Flask, render_template, request
from config import SQLALCHEMY_DATABASE_URI
from models import db, 顧客, 商品, 注文, 注文明細

app = Flask(__name__)
app.config.from_object('config')  # config.pyから設定を読み込む
db.init_app(app)

# ホーム画面
@app.route('/')
def home():
    return 'Welcome to the注文管理アプリ!'

if __name__ == '__main__':
    app.run(debug=True)
