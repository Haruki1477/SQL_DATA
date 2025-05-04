# gui_product_manage.py
import tkinter as tk
from tkinter import ttk, messagebox
import db

class ProductManageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("商品管理")

        # 商品リストの表示
        self.products = self.get_product_list()
        self.tree = ttk.Treeview(root, columns=("商品ID", "商品名", "単価"), show="headings")
        self.tree.heading("商品ID", text="商品ID")
        self.tree.heading("商品名", text="商品名")
        self.tree.heading("単価", text="単価")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for product in self.products:
            self.tree.insert("", "end", values=product)

        # 編集・削除ボタン
        edit_button = tk.Button(root, text="編集", command=self.edit_product)
        edit_button.pack(side="left", padx=10)

        delete_button = tk.Button(root, text="削除", command=self.delete_product)
        delete_button.pack(side="left", padx=10)

    def get_product_list(self):
        products = []
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 商品ID, 商品名, 単価 FROM 商品")
        products = cur.fetchall()
        cur.close()
        conn.close()
        return products

    def edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("選択エラー", "商品を選択してください")
            return

        product_id = self.tree.item(selected_item)["values"][0]
        name = self.tree.item(selected_item)["values"][1]
        price = self.tree.item(selected_item)["values"][2]

        # 編集画面を表示
        edit_window = tk.Toplevel(self.root)
        edit_window.title("商品編集")

        tk.Label(edit_window, text="商品名").pack()
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, name)
        name_entry.pack()

        tk.Label(edit_window, text="単価").pack()
        price_entry = tk.Entry(edit_window)
        price_entry.insert(0, price)
        price_entry.pack()

        def save_changes():
            new_name = name_entry.get()
            try:
                new_price = int(price_entry.get())
                if new_price <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("入力エラー", "単価は正の整数で入力してください")
                return

            db.update_product(product_id, new_name, new_price)
            messagebox.showinfo("成功", "商品が更新されました")
            edit_window.destroy()
            self.refresh_product_list()

        save_button = tk.Button(edit_window, text="保存", command=save_changes)
        save_button.pack()

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("選択エラー", "商品を選択してください")
            return

        product_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("確認", f"商品ID {product_id} を削除しますか？")
        if confirm:
            db.delete_product(product_id)
            messagebox.showinfo("成功", "商品が削除されました")
            self.refresh_product_list()

    def refresh_product_list(self):
        # 商品リストを更新
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.products = self.get_product_list()
        for product in self.products:
            self.tree.insert("", "end", values=product)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductManageApp(root)
    root.mainloop()
