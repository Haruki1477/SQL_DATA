# gui_product.py
import tkinter as tk
from tkinter import messagebox
import db

def register_product():
    name = name_entry.get()
    try:
        price = int(price_entry.get())
        if price <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("入力エラー", "単価は正の整数で入力してください")
        return

    if not name:
        messagebox.showwarning("入力エラー", "商品名を入力してください")
        return

    db.insert_product(name, price)
    messagebox.showinfo("成功", "商品を登録しました")
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

# GUI構築
window = tk.Tk()
window.title("商品登録")

tk.Label(window, text="商品名").grid(row=0, column=0)
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1)

tk.Label(window, text="単価").grid(row=1, column=0)
price_entry = tk.Entry(window)
price_entry.grid(row=1, column=1)

register_button = tk.Button(window, text="登録", command=register_product)
register_button.grid(row=2, column=0, columnspan=2)

window.mainloop()
