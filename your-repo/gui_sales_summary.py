import tkinter as tk
from tkinter import ttk
import db

class SalesSummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("売上集計")

        tab_control = ttk.Notebook(root)

        self.date_tab = ttk.Frame(tab_control)
        self.customer_tab = ttk.Frame(tab_control)

        tab_control.add(self.date_tab, text="日別")
        tab_control.add(self.customer_tab, text="顧客別")
        tab_control.pack(expand=1, fill="both")

        self.setup_date_tab()
        self.setup_customer_tab()

    def setup_date_tab(self):
        tree = ttk.Treeview(self.date_tab, columns=("注文日", "売上合計"), show="headings")
        tree.heading("注文日", text="注文日")
        tree.heading("売上合計", text="売上合計")
        tree.pack(fill=tk.BOTH, expand=True)

        rows = db.get_sales_summary_by_date()
        for row in rows:
            tree.insert("", tk.END, values=row)

    def setup_customer_tab(self):
        tree = ttk.Treeview(self.customer_tab, columns=("氏名", "売上合計"), show="headings")
        tree.heading("氏名", text="氏名")
        tree.heading("売上合計", text="売上合計")
        tree.pack(fill=tk.BOTH, expand=True)

        rows = db.get_sales_summary_by_customer()
        for row in rows:
            tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesSummaryApp(root)
    root.mainloop()
