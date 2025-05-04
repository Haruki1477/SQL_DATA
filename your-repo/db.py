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

def get_orders_with_details():
    conn = get_connection()
    cur = conn.cursor()
    query = """
    SELECT
        o.注文ID,
        o.注文日,
        c.氏名 AS 顧客名,
        p.商品名,
        p.単価,
        d.数量,
        (p.単価 * d.数量) AS 金額
    FROM 注文 o
    JOIN 顧客 c ON o.顧客ID = c.顧客ID
    JOIN 注文明細 d ON o.注文ID = d.注文ID
    JOIN 商品 p ON d.商品ID = p.商品ID
    ORDER BY o.注文ID, p.商品ID;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def update_product(product_id, name, price):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE 商品 SET 商品名 = %s, 単価 = %s WHERE 商品ID = %s",
            (name, price, product_id)
        )
        conn.commit()
    except Exception as e:
        print("エラー:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def delete_product(product_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM 商品 WHERE 商品ID = %s", (product_id,))
        conn.commit()
    except Exception as e:
        print("エラー:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def update_order(order_id, customer_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE 注文 SET 顧客ID = %s WHERE 注文ID = %s",
            (customer_id, order_id)
        )
        conn.commit()
    except Exception as e:
        print("エラー:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def delete_order(order_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM 注文明細 WHERE 注文ID = %s", (order_id,))
        cur.execute("DELETE FROM 注文 WHERE 注正ID = %s", (order_id,))
        conn.commit()
    except Exception as e:
        print("エラー:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

