import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import date

class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("注文登録")

        self.selected_products = []

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        # 顧客選択
        ttk.Label(frame, text="顧客:").grid(row=0, column=0)
        self.customers = db.get_customer_list()  # [(id, name), ...]
        self.customer_var = tk.StringVar()
        customer_names = [f"{c[0]}: {c[1]}" for c in self.customers]
        self.customer_cb = ttk.Combobox(frame, values=customer_names, textvariable=self.customer_var)
        self.customer_cb.grid(row=0, column=1, padx=5)

        # 商品選択
        ttk.Label(frame, text="商品:").grid(row=1, column=0)
        self.products = db.get_product_list()  # [(id, name, price), ...]
        self.product_var = tk.StringVar()
        product_names = [f"{p[0]}: {p[1]} ({p[2]}円)" for p in self.products]
        self.product_cb = ttk.Combobox(frame, values=product_names, textvariable=self.product_var)
        self.product_cb.grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="数量:").grid(row=1, column=2)
        self.qty_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.qty_var, width=5).grid(row=1, column=3)

        ttk.Button(frame, text="追加", command=self.add_to_list).grid(row=1, column=4, padx=5)

        # 注文明細のリスト
        self.tree = ttk.Treeview(self.root, columns=("商品ID", "商品名", "数量"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        ttk.Button(self.root, text="注文を登録", command=self.submit_order).pack()

    def add_to_list(self):
        try:
            product_index = self.product_cb.current()
            product = self.products[product_index]
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except:
            messagebox.showerror("エラー", "商品と数量を正しく入力してください")
            return

        self.selected_products.append((product[0], product[1], qty))  # 商品ID, 名, 数量
        self.tree.insert("", "end", values=(product[0], product[1], qty))
        self.qty_var.set("")

    def submit_order(self):
        try:
            customer_index = self.customer_cb.current()
            customer_id = self.customers[customer_index][0]
        except:
            messagebox.showerror("エラー", "顧客を選択してください")
            return

        if not self.selected_products:
            messagebox.showerror("エラー", "商品が選択されていません")
            return

        order_date = date.today()
        order_id = db.add_order(customer_id, order_date)

        for product_id, _, qty in self.selected_products:
            db.add_order_detail(order_id, product_id, qty)

        messagebox.showinfo("成功", f"注文 {order_id} を登録しました")
        self.tree.delete(*self.tree.get_children())
        self.selected_products.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()
