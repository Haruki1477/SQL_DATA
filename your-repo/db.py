# db.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="test",
        user="postgres",
        password="haru0707"
    )

def insert_customer(name, email):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO 顧客 (氏名, メールアドレス) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()
    except Exception as e:
        print("エラー:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def insert_product(name, price):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO 商品 (商品名, 単価) VALUES (%s, %s)",
            (name, price)
        )
        conn.commit()
    except Exception as e:
        print("エラー:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
