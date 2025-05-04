import tkinter as tk
from tkinter import ttk
import subprocess
import os
import sys

class MainLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("販売管理システム メニュー")
        self.root.geometry("400x300")

        ttk.Label(root, text="機能を選んでください", font=("Arial", 14)).pack(pady=20)

        buttons = [
            ("顧客管理", "gui_customer.py"),
            ("商品管理", "gui_product.py"),
            ("注文管理", "gui_order.py"),
            ("売上集計", "gui_sales_summary.py"),
        ]

        for text, file in buttons:
            ttk.Button(root, text=text, width=30, command=lambda f=file: self.run_file(f)).pack(pady=5)

    def run_file(self, filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, filename)
        subprocess.Popen([sys.executable, full_path])


if __name__ == "__main__":
    root = tk.Tk()
    app = MainLauncher(root)
    root.mainloop()
