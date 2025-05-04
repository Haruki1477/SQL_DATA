# gui_order_manage.py
import tkinter as tk
from tkinter import ttk, messagebox
import db

class OrderManageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("注文管理")

        # 注文リストの表示
        self.orders = self.get_order_list()
        self.tree = ttk.Treeview(root, columns=("注文ID", "顧客名", "注文日"), show="headings")
        self.tree.heading("注文ID", text="注文ID")
        self.tree.heading("顧客名", text="顧客名")
        self.tree.heading("注文日", text="注文日")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for order in self.orders:
            self.tree.insert("", "end", values=order)

        # 編集・削除ボタン
        edit_button = tk.Button(root, text="編集", command=self.edit_order)
        edit_button.pack(side="left", padx=10)

        delete_button = tk.Button(root, text="削除", command=self.delete_order)
        delete_button.pack(side="left", padx=10)

    def get_order_list(self):
        orders = []
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 注文ID, 氏名, 注文日 
            FROM 注文 o
            JOIN 顧客 c ON o.顧客ID = c.顧客ID
        """)
        orders = cur.fetchall()
        cur.close()
        conn.close()
        return orders

    def edit_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("選択エラー", "注文を選択してください")
            return

        order_id = self.tree.item(selected_item)["values"][0]
        customer_name = self.tree.item(selected_item)["values"][1]

        # 顧客選択ウィンドウを表示
        edit_window = tk.Toplevel(self.root)
        edit_window.title("注文編集")

        tk.Label(edit_window, text="顧客名").pack()
        customers = db.get_customers()  # 顧客リストを取得
        customer_var = tk.StringVar()
        customer_menu = tk.OptionMenu(edit_window, customer_var, *[f"{c[0]}: {c[1]}" for c in customers])
        customer_menu.pack()

        # 顧客名のデフォルト値設定
        customer_var.set(f"{self.get_customer_id_by_name(customer_name)}: {customer_name}")

        def save_changes():
            new_customer_id = int(customer_var.get().split(":")[0])
            db.update_order(order_id, new_customer_id)
            messagebox.showinfo("成功", "注文が更新されました")
            edit_window.destroy()
            self.refresh_order_list()

        save_button = tk.Button(edit_window, text="保存", command=save_changes)
        save_button.pack()

    def delete_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("選択エラー", "注文を選択してください")
            return

        order_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("確認", f"注文ID {order_id} を削除しますか？")
        if confirm:
            db.delete_order(order_id)
            messagebox.showinfo("成功", "注文が削除されました")
            self.refresh_order_list()

    def refresh_order_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.orders = self.get_order_list()
        for order in self.orders:
            self.tree.insert("", "end", values=order)

    def get_customer_id_by_name(self, name):
        for customer_id, customer_name in db.get_customers():
            if customer_name == name:
                return customer_id

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderManageApp(root)
    root.mainloop()
