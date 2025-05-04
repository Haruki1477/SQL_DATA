import tkinter as tk
from tkinter import ttk
import db

class CustomerSalesSummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("売上集計（顧客別）")

        self.tree = ttk.Treeview(root, columns=("顧客名", "売上合計"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.load_data()

    def load_data(self):
        rows = db.get_sales_summary_by_customer()
        for row in rows:
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerSalesSummaryApp(root)
    root.mainloop()
