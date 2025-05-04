import tkinter as tk
from tkinter import ttk, messagebox
import db  # 既存のDB接続ファイル

class EditProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("商品検索・編集")

        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        # 検索欄
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="検索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="検索", command=self.search_products).pack(side=tk.LEFT)

        # 商品一覧
        self.tree = ttk.Treeview(self.root, columns=("id", "name", "price"), show="headings", height=10)
        for col in ("id", "name", "price"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # 編集欄
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="商品名").grid(row=0, column=0, padx=5, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1)

        ttk.Label(form_frame, text="金額").grid(row=1, column=0, padx=5, pady=2)
        self.price_var = tk.DoubleVar()
        ttk.Entry(form_frame, textvariable=self.price_var).grid(row=1, column=1)

        ttk.Button(self.root, text="更新", command=self.update_product).pack(pady=5)

    def load_products(self, keyword=""):
        self.tree.delete(*self.tree.get_children())
        products = db.search_products(keyword)
        for p in products:
            self.tree.insert("", "end", values=p)

    def search_products(self):
        keyword = self.search_var.get()
        self.load_products(keyword)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]
        self.name_var.set(values[1])
        self.price_var.set(values[2])

    def update_product(self):
        if not hasattr(self, "selected_id"):
            messagebox.showwarning("警告", "商品を選択してください。")
            return
        name = self.name_var.get()
        price = self.price_var.get()
        db.update_product(self.selected_id, name, price)
        messagebox.showinfo("成功", "更新しました。")
        self.load_products()

if __name__ == "__main__":
    root = tk.Tk()
    app = EditProductApp(root)
    root.mainloop()
