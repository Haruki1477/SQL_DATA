import tkinter as tk
from tkinter import ttk, messagebox
import db  # あなたの既存DB接続モジュールを想定

class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("顧客管理")

        self.create_widgets()
        self.load_customers()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="顧客名:").grid(row=0, column=0)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=20).grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="メールアドレス:").grid(row=0, column=2)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=25).grid(row=0, column=3, padx=5)

        ttk.Button(frame, text="登録", command=self.add_customer).grid(row=0, column=4, padx=5)

        # 一覧表示
        self.tree = ttk.Treeview(self.root, columns=("id", "name", "email"), show="headings")
        self.tree.heading("id", text="顧客ID")
        self.tree.heading("name", text="顧客名")
        self.tree.heading("email", text="メールアドレス")
        self.tree.pack(pady=10)

    def add_customer(self):
        name = self.name_var.get()
        email = self.email_var.get()

        if name == "" or email == "":
            messagebox.showerror("エラー", "全ての項目を入力してください")
            return

        try:
            db.add_customer(name, email)
            messagebox.showinfo("成功", "顧客を登録しました")
            self.name_var.set("")
            self.email_var.set("")
            self.load_customers()
        except Exception as e:
            messagebox.showerror("エラー", str(e))

    def load_customers(self):
        self.tree.delete(*self.tree.get_children())
        for row in db.get_all_customers():
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()
