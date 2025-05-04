import tkinter as tk
from tkinter import ttk
import db

class SalesSummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("売上集計（日付別）")

        self.tree = ttk.Treeview(root, columns=("注文日", "売上合計"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.load_data()

    def load_data(self):
        rows = db.get_sales_summary_by_date()
        for row in rows:
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesSummaryApp(root)
    root.mainloop()
