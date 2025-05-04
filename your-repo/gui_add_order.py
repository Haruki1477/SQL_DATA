# gui_order.py
import tkinter as tk
from tkinter import messagebox
import db

class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("注文登録")

        # 顧客選択
        tk.Label(root, text="顧客").grid(row=0, column=0)
        self.customers = db.get_customers()
        self.customer_var = tk.StringVar()
        self.customer_menu = tk.OptionMenu(root, self.customer_var, *[f"{c[0]}: {c[1]}" for c in self.customers])
        self.customer_menu.grid(row=0, column=1)

        # 商品リスト
        self.products = db.get_products()
        self.product_vars = []
        self.quantity_entries = []

        tk.Label(root, text="商品").grid(row=1, column=0)
        frame = tk.Frame(root)
        frame.grid(row=1, column=1)
        for i, (pid, pname, price) in enumerate(self.products):
            var = tk.IntVar()
            cb = tk.Checkbutton(frame, text=f"{pname} ({price}円)", variable=var)
            cb.grid(row=i, column=0, sticky='w')
            qty = tk.Entry(frame, width=5)
            qty.insert(0, "1")
            qty.grid(row=i, column=1)
            self.product_vars.append((pid, var))
            self.quantity_entries.append(qty)

        # 登録ボタン
        tk.Button(root, text="注文登録", command=self.submit_order).grid(row=2, column=0, columnspan=2)

    def submit_order(self):
        selected_customer = self.customer_var.get()
        if not selected_customer:
            messagebox.showwarning("エラー", "顧客を選択してください")
            return

        customer_id = int(selected_customer.split(":")[0])
        items = []
        for (pid, var), qty_entry in zip(self.product_vars, self.quantity_entries):
            if var.get():
                try:
                    qty = int(qty_entry.get())
                    if qty <= 0:
                        raise ValueError
                    items.append((pid, qty))
                except ValueError:
                    messagebox.showerror("エラー", f"商品ID {pid} の数量が不正です")
                    return

        if not items:
            messagebox.showwarning("エラー", "1つ以上の商品を選択してください")
            return

        db.insert_order(customer_id, items)
        messagebox.showinfo("成功", "注文を登録しました")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()
