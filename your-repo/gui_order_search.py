import tkinter as tk
from tkinter import ttk, messagebox
import db

class OrderSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("注文検索・編集")

        self.search_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.search_var).pack(pady=5, padx=5)
        ttk.Button(root, text="検索", command=self.search_orders).pack()

        self.tree = ttk.Treeview(root, columns=("注文ID", "顧客名", "注文日"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        ttk.Button(root, text="注文を削除", command=self.delete_order).pack(pady=5)

        self.search_orders()

    def search_orders(self):
        keyword = self.search_var.get()
        results = db.search_orders(keyword)
        self.tree.delete(*self.tree.get_children())
        for row in results:
            self.tree.insert("", "end", values=row)

    def delete_order(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("警告", "注文を選択してください")
            return
        values = self.tree.item(selected, "values")
        if messagebox.askyesno("確認", f"注文ID {values[0]} を削除しますか？（明細も削除されます）"):
            db.delete_order(values[0])
            self.search_orders()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderSearchApp(root)
    root.mainloop()
