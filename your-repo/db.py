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
def get_customers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 顧客ID, 氏名 FROM 顧客")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 商品ID, 商品名, 単価 FROM 商品")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def insert_order(customer_id, items):  # items: [(商品ID, 数量)]
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO 注文 (顧客ID) VALUES (%s) RETURNING 注文ID", (customer_id,))
        order_id = cur.fetchone()[0]

        for product_id, quantity in items:
            cur.execute(
                "INSERT INTO 注文明細 (注文ID, 商品ID, 数量) VALUES (%s, %s, %s)",
                (order_id, product_id, quantity)
            )
        conn.commit()
    except Exception as e:
        print("エラー:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
