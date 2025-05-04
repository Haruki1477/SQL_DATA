from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 顧客テーブル
class 顧客(db.Model):
    __tablename__ = '顧客'
    顧客ID = db.Column(db.Integer, primary_key=True)
    氏名 = db.Column(db.String(100), nullable=False)

    注文 = db.relationship('注文', backref='顧客', lazy=True)

# 商品テーブル
class 商品(db.Model):
    __tablename__ = '商品'
    商品ID = db.Column(db.Integer, primary_key=True)
    商品名 = db.Column(db.String(100), nullable=False)
    単価 = db.Column(db.Integer, nullable=False)

    注文明細 = db.relationship('注文明細', backref='商品', lazy=True)

# 注文テーブル
class 注文(db.Model):
    __tablename__ = '注文'
    注文ID = db.Column(db.Integer, primary_key=True)
    顧客ID = db.Column(db.Integer, db.ForeignKey('顧客.顧客ID'), nullable=False)
    注文日 = db.Column(db.Date, nullable=False)

    注文明細 = db.relationship('注文明細', backref='注文', lazy=True)

# 注文明細テーブル（複合キー）
class 注文明細(db.Model):
    __tablename__ = '注文明細'
    注文ID = db.Column(db.Integer, db.ForeignKey('注文.注文ID'), primary_key=True)
    商品ID = db.Column(db.Integer, db.ForeignKey('商品.商品ID'), primary_key=True)
    数量 = db.Column(db.Integer, nullable=False)

