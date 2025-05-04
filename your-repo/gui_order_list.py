# gui_order_list.py
import tkinter as tk
from tkinter import ttk
import db

def show_orders():
    data = db.get_orders_with_details()

    tree.delete(*tree.get_children())

    last_order_id = None
    for row in data:
        order_id, order_date, customer, product, price, qty, total = row
        if order_id != last_order_id:
            tree.insert("", "end", values=(f"注文ID: {order_id}", "", "", "", "", "", ""))
        tree.insert("", "end", values=("", order_date, customer, product, price, qty, total))
        last_order_id = order_id

# GUI構築
root = tk.Tk()
root.title("注文一覧")

cols = ("", "注文日", "顧客", "商品名", "単価", "数量", "金額")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.pack(fill=tk.BOTH, expand=True)

refresh_button = tk.Button(root, text="再読み込み", command=show_orders)
refresh_button.pack()

show_orders()
root.mainloop()
