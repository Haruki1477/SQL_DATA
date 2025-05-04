import tkinter as tk
from tkinter import ttk, messagebox
import db

class ProductSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("商品検索・編集")

        self.search_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.search_var).pack(pady=5, padx=5)
        ttk.Button(root, text="検索", command=self.search_products).pack()

        self.tree = ttk.Treeview(root, columns=("ID", "商品名", "単価"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        btn_frame = ttk.Frame(root)
        btn_frame.pack()
        ttk.Button(btn_frame, text="編集", command=self.edit_product).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="削除", command=self.delete_product).grid(row=0, column=1, padx=5)

        self.search_products()

    def search_products(self):
        keyword = self.search_var.get()
        results = db.search_products_by_name(keyword)
        self.tree.delete(*self.tree.get_children())
        for row in results:
            self.tree.insert("", "end", values=row)

    def edit_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("警告", "商品を選択してください")
            return
        values = self.tree.item(selected, "values")
        self.open_edit_window(values)

    def open_edit_window(self, product):
        top = tk.Toplevel(self.root)
        top.title("商品編集")

        tk.Label(top, text="商品名").grid(row=0, column=0)
        name_var = tk.StringVar(value=product[1])
        tk.Entry(top, textvariable=name_var).grid(row=0, column=1)

        tk.Label(top, text="単価").grid(row=1, column=0)
        price_var = tk.StringVar(value=product[2])
        tk.Entry(top, textvariable=price_var).grid(row=1, column=1)

        def save():
            try:
                db.update_product(product[0], name_var.get(), int(price_var.get()))
                top.destroy()
                self.search_products()
            except ValueError:
                messagebox.showerror("エラー", "単価は整数で入力してください")

        tk.Button(top, text="保存", command=save).grid(row=2, column=0, columnspan=2, pady=5)

    def delete_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("警告", "商品を選択してください")
            return
        values = self.tree.item(selected, "values")
        if messagebox.askyesno("確認", f"{values[1]} を削除してよろしいですか？"):
            db.delete_product(values[0])
            self.search_products()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductSearchApp(root)
    root.mainloop()
