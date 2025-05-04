import tkinter as tk
from tkinter import ttk, messagebox
import db  # 既存のDBモジュールを想定

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("商品管理")

        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        # 入力欄
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="商品名:").grid(row=0, column=0)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=20).grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="単価:").grid(row=0, column=2)
        self.price_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.price_var, width=10).grid(row=0, column=3, padx=5)

        ttk.Button(frame, text="追加", command=self.add_product).grid(row=0, column=4, padx=5)

        # 商品一覧
        self.tree = ttk.Treeview(self.root, columns=("id", "name", "price"), show="headings")
        self.tree.heading("id", text="商品ID")
        self.tree.heading("name", text="商品名")
        self.tree.heading("price", text="単価")
        self.tree.pack(pady=10)

    def add_product(self):
        name = self.name_var.get()
        try:
            price = int(self.price_var.get())
        except ValueError:
            messagebox.showerror("エラー", "単価は整数で入力してください")
            return

        if name == "" or price <= 0:
            messagebox.showerror("エラー", "正しい情報を入力してください")
            return

        db.add_product(name, price)
        messagebox.showinfo("追加", "商品を追加しました")
        self.name_var.set("")
        self.price_var.set("")
        self.load_products()

    def load_products(self):
        self.tree.delete(*self.tree.get_children())
        for row in db.get_all_products():
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()
