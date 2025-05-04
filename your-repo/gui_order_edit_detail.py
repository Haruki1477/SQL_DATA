import tkinter as tk
from tkinter import ttk, messagebox
import db  # 既存のDBモジュールを想定

class OrderDetailEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("注文明細 編集")

        self.create_widgets()

    def create_widgets(self):
        # 注文ID入力
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="注文ID:").pack(side=tk.LEFT)
        self.order_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.order_id_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="検索", command=self.load_details).pack(side=tk.LEFT)

        # 明細表示
        self.tree = ttk.Treeview(self.root, columns=("product", "quantity"), show="headings")
        self.tree.heading("product", text="商品ID")
        self.tree.heading("quantity", text="数量")
        self.tree.pack(pady=10)

        self.tree.bind("<Double-1>", self.edit_quantity)

        ttk.Button(self.root, text="更新", command=self.update_details).pack(pady=5)

    def load_details(self):
        self.tree.delete(*self.tree.get_children())
        self.details = db.get_order_details(self.order_id_var.get())
        for row in self.details:
            self.tree.insert("", "end", values=row)

    def edit_quantity(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        product_id, quantity = item['values']
        new_qty = tk.simpledialog.askinteger("数量編集", f"{product_id} の新しい数量：", initialvalue=quantity)
        if new_qty and new_qty > 0:
            self.tree.item(selected[0], values=(product_id, new_qty))

    def update_details(self):
        updated = []
        for row in self.tree.get_children():
            product_id, quantity = self.tree.item(row)['values']
            updated.append((self.order_id_var.get(), product_id, quantity))
        db.update_order_details(updated)
        messagebox.showinfo("完了", "更新されました。")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderDetailEditor(root)
    root.mainloop()
