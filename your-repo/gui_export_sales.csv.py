import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import db
import csv

class SalesCSVExportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("売上CSV出力（期間指定）")

        # 日付入力
        frame = ttk.Frame(root)
        frame.pack(pady=10)
        ttk.Label(frame, text="開始日 (YYYY-MM-DD):").grid(row=0, column=0)
        ttk.Label(frame, text="終了日 (YYYY-MM-DD):").grid(row=0, column=2)

        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()
        ttk.Entry(frame, textvariable=self.start_date).grid(row=0, column=1)
        ttk.Entry(frame, textvariable=self.end_date).grid(row=0, column=3)

        ttk.Button(root, text="検索・表示", command=self.load_data).pack()
        ttk.Button(root, text="CSVに保存", command=self.export_csv).pack(pady=5)

        self.tree = ttk.Treeview(root, columns=("注文日", "顧客名", "商品名", "数量", "単価", "合計"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.data = []

    def load_data(self):
        self.data = db.get_sales_data_by_period(self.start_date.get(), self.end_date.get())
        self.tree.delete(*self.tree.get_children())
        for row in self.data:
            self.tree.insert("", "end", values=row)

    def export_csv(self):
        if not self.data:
            messagebox.showwarning("警告", "出力するデータがありません。")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["注文日", "顧客名", "商品名", "数量", "単価", "合計"])
            for row in self.data:
                writer.writerow(row)
        messagebox.showinfo("完了", f"CSVファイルを保存しました: {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesCSVExportApp(root)
    root.mainloop()
