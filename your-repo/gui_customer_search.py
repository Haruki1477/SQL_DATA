import tkinter as tk
from tkinter import ttk, messagebox
import db

class CustomerSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("顧客検索・編集")

        self.search_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.search_var).pack(pady=5, padx=5)
        ttk.Button(root, text="検索", command=self.search_customers).pack()

        self.tree = ttk.Treeview(root, columns=("ID", "氏名", "メール"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        btn_frame = ttk.Frame(root)
        btn_frame.pack()
        ttk.Button(btn_frame, text="編集", command=self.edit_customer).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="削除", command=self.delete_customer).grid(row=0, column=1, padx=5)

        self.search_customers()

    def search_customers(self):
        keyword = self.search_var.get()
        results = db.search_customers_by_name(keyword)
        self.tree.delete(*self.tree.get_children())
        for row in results:
            self.tree.insert("", "end", values=row)

    def edit_customer(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("警告", "顧客を選択してください")
            return
        values = self.tree.item(selected, "values")
        self.open_edit_window(values)

    def open_edit_window(self, customer):
        top = tk.Toplevel(self.root)
        top.title("顧客編集")

        tk.Label(top, text="氏名").grid(row=0, column=0)
        name_var = tk.StringVar(value=customer[1])
        tk.Entry(top, textvariable=name_var).grid(row=0, column=1)

        tk.Label(top, text="メール").grid(row=1, column=0)
        email_var = tk.StringVar(value=customer[2])
        tk.Entry(top, textvariable=email_var).grid(row=1, column=1)

        def save():
            db.update_customer(customer[0], name_var.get(), email_var.get())
            top.destroy()
            self.search_customers()

        tk.Button(top, text="保存", command=save).grid(row=2, column=0, columnspan=2, pady=5)

    def delete_customer(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("警告", "顧客を選択してください")
            return
        values = self.tree.item(selected, "values")
        if messagebox.askyesno("確認", f"{values[1]} を削除してよろしいですか？"):
            db.delete_customer(values[0])
            self.search_customers()

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerSearchApp(root)
    root.mainloop()
