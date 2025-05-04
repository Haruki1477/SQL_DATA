# gui_customer.py
import tkinter as tk
from tkinter import messagebox
import db  # db.pyをインポート

def register_customer():
    name = name_entry.get()
    email = email_entry.get()
    if not name or not email:
        messagebox.showwarning("入力エラー", "氏名とメールアドレスを入力してください")
        return
    db.insert_customer(name, email)
    messagebox.showinfo("成功", "顧客を登録しました")
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# ウィンドウ作成
window = tk.Tk()
window.title("顧客登録")

# ラベルと入力欄
tk.Label(window, text="氏名").grid(row=0, column=0)
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1)

tk.Label(window, text="メールアドレス").grid(row=1, column=0)
email_entry = tk.Entry(window)
email_entry.grid(row=1, column=1)

# 登録ボタン
register_button = tk.Button(window, text="登録", command=register_customer)
register_button.grid(row=2, column=0, columnspan=2)

window.mainloop()
