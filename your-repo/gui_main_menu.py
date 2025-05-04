import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
from tkinter import messagebox


class MainMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("販売管理メニュー")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        ttk.Label(frame, text="メニュー", font=("Helvetica", 16)).pack(pady=10)

        buttons = [
            ("顧客登録", "gui_customer.py"),
            ("商品登録", "gui_product.py"),
            ("注文登録", "gui_order_input.py"),
            ("売上集計", "gui_sales_summary.py"),
        ]

        for text, script in buttons:
            ttk.Button(frame, text=text, command=lambda s=script: self.open_script(s)).pack(pady=5, fill=tk.X)

        ttk.Button(frame, text="終了", command=self.root.quit).pack(pady=10, fill=tk.X)

    def open_script(self, script_name):
        # Pythonスクリプトを別プロセスで開く
        full_path = os.path.join(os.path.dirname(__file__), script_name)
        if os.path.exists(full_path):
            subprocess.Popen([sys.executable, full_path])
        else:
            tk.messagebox.showerror("エラー", f"{script_name} が見つかりません")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenuApp(root)
    root.mainloop()
