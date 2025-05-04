import tkinter as tk
from tkinter import ttk, messagebox
import db

class OrderInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("注文入力")

        self.customers = db.get_customers()
        self.products = db.get_products()
        self.order_items = []

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="顧客:").grid(row=0, column=0)
        self.customer_cb = ttk.Combobox(frame, values=[f"{c[1]} (ID:{c[0]})" for c in self.customers], state="readonly")
        self.customer_cb.grid(row=0, column=1, columnspan=2, sticky="ew")

        ttk.Label(frame, text="商品:").grid(row=1, column=0)
        self.product_cb = ttk.Combobox(frame, values=[f"{p[1]} (¥{p[2]})" for p in self.products], state="readonly")
        self.product_cb.grid(row=1, column=1)

        ttk.Label(frame, text="数量:").grid(row=1, column=2)
        self.qty_entry = ttk.Entry(frame, width=5)
        self.qty_entry.grid(row=1, column=3)

        ttk.Button(frame, text="追加", command=self.add_item).grid(row=1, column=4)

        self.tree = ttk.Treeview(self.root, columns=("商品", "数量"), show="headings")
        self.tree.heading("商品", text="商品")
        self.tree.heading("数量", text="数量")
        self.tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        ttk.Button(self.root, text="注文を登録", command=self.submit_order).pack(pady=10)

    def add_item(self):
        index = self.product_cb.current()
        qty = self.qty_entry.get()
        if index == -1 or not qty.isdigit() or int(qty) <= 0:
            messagebox.showerror("エラー", "商品と正しい数量を入力してください")
            return

        product = self.products[index]
        self.order_items.append((product[0], int(qty)))
        self.tree.insert("", tk.END, values=(product[1], qty))
        self.qty_entry.delete(0, tk.END)

    def submit_order(self):
        customer_index = self.customer_cb.current()
        if customer_index == -1 or not self.order_items:
            messagebox.showerror("エラー", "顧客と注文明細を入力してください")
            return

        顧客ID = self.customers[customer_index][0]
        db.insert_order(顧客ID, self.order_items)
        messagebox.showinfo("完了", "注文を登録しました")
        self.tree.delete(*self.tree.get_children())
        self.order_items.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderInputApp(root)
    root.mainloop()
