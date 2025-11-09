import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------ LOAD CSV DATA ------------------
try:
    df = pd.read_csv("sales_data.csv")
except FileNotFoundError:
    messagebox.showerror("File Error", "sales_data.csv not found! Please place it in the same folder.")
    exit()

# ------------------ DATA EXTRACTION ------------------
months = df["Month"]
sales_revenue = df["Revenue"]
quantities = df["Quantity"]

# ------------------ MERGE SORT FUNCTION ------------------
def merge_sort(data_list, key=lambda x: x, reverse=False):
    if len(data_list) <= 1:
        return data_list

    mid = len(data_list) // 2
    left = merge_sort(data_list[:mid], key, reverse)
    right = merge_sort(data_list[mid:], key, reverse)
    return merge(left, right, key, reverse)

def merge(left, right, key, reverse):
    sorted_list = []
    while left and right:
        if (key(left[0]) < key(right[0])) ^ reverse:
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    sorted_list.extend(left if left else right)
    return sorted_list

# ------------------ MAIN WINDOW SETUP ------------------
root = tk.Tk()
root.title("SmartSales Dashboard - Desmond Company")
root.geometry("1500x900")
root.config(bg="#eef5f9")

# ------------------ TITLE ------------------
title = tk.Label(root, text="📊 SmartSales Dashboard - Desmond Company",
                 font=("Arial", 26, "bold"), bg="#eef5f9", fg="#1f4e79")
title.pack(pady=20)

# ------------------ MAIN CONTAINER ------------------
main_container = tk.Frame(root, bg="#eef5f9")
main_container.pack(fill="both", expand=True, padx=15, pady=10)

# ------------------ SIDEBAR BUTTON FRAME ------------------
sidebar = tk.Frame(main_container, bg="#1f4e79", width=250)
sidebar.pack(side="left", fill="y", padx=(0, 15), pady=10)
sidebar.pack_propagate(False)

btn_style = {
    "font": ("Arial", 13, "bold"),
    "width": 22,
    "height": 2,
    "relief": "flat",
    "bd": 0
}

def create_button(parent, text, color, command):
    return tk.Button(
        parent, text=text, bg=color, fg="white",
        activebackground="#333333", activeforeground="white",
        cursor="hand2", command=command, **btn_style
    )

# ------------------ CHART FRAME ------------------
chart_frame = tk.Frame(main_container, bg="#ffffff", bd=4, relief="ridge")
chart_frame.pack(side="right", fill="both", expand=True)
chart_frame.pack_propagate(False)

# ------------------ TABLE FRAME ------------------
table_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
table_frame.pack(padx=20, pady=(5, 15), fill="x")

table_title = tk.Label(table_frame, text="📋 Monthly Sales Data",
                       font=("Arial", 18, "bold"), bg="#ffffff", fg="#333333")
table_title.pack(pady=8)

columns = list(df.columns)
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=9)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150, anchor='center')

for _, row in df.iterrows():
    table.insert("", "end", values=list(row))

table.pack(padx=10, pady=10, fill="x")

# ------------------ HELPER FUNCTION ------------------
def clear_chart():
    for widget in chart_frame.winfo_children():
        widget.destroy()

# ------------------ VISUALIZATION FUNCTIONS ------------------
def show_line_chart():
    clear_chart()
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.plot(months, sales_revenue, marker='o', color='#0073e6', linewidth=2)
    ax.set_title("Sales Trend Over Time", fontsize=16)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def show_area_chart():
    clear_chart()
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.fill_between(months, sales_revenue, color='#6fcf97', alpha=0.6)
    ax.plot(months, sales_revenue, color='#27ae60', linewidth=2)
    ax.set_title("Area Chart - Sales Growth", fontsize=16)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def show_bar_chart():
    clear_chart()
    cat_sales = df.groupby("Category")["Revenue"].sum()
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.bar(cat_sales.index, cat_sales.values, color='#f39c12')
    ax.set_title("Sales by Product Category", fontsize=16)
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Total Sales ($)")
    ax.grid(axis='y')
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def show_pie_chart():
    clear_chart()
    seg_sales = df.groupby("CustomerSegment")["Revenue"].sum()
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(seg_sales.values, labels=seg_sales.index, autopct='%1.1f%%',
           startangle=90, colors=['#e74c3c', '#f1c40f', '#5dade2', '#58d68d'])
    ax.set_title("Sales Distribution by Customer Segment", fontsize=16)
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

# ------------------ SORTED PAGE (MERGE SORT) ------------------
def show_sorted_page():
    sorted_window = tk.Toplevel(root)
    sorted_window.title("Sorted Data Insights - Merge Sort")
    sorted_window.geometry("1200x800")
    sorted_window.config(bg="#f9f9f9")

    title = tk.Label(sorted_window, text="🔍 Sorted Sales Insights (Merge Sort)",
                     font=("Arial", 20, "bold"), bg="#f9f9f9", fg="#1f4e79")
    title.pack(pady=15)

    frame = tk.Frame(sorted_window, bg="#ffffff", bd=2, relief="solid")
    frame.pack(fill="both", expand=True, padx=15, pady=15)
    frame.pack_propagate(False)

    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    def show_highest_revenue():
        clear_frame()
        monthly_data = df.groupby("Month")["Revenue"].sum().reset_index()
        sorted_data = merge_sort(monthly_data.values.tolist(), key=lambda x: x[1], reverse=True)
        sorted_df = pd.DataFrame(sorted_data, columns=["Month", "Revenue"])
        fig, ax = plt.subplots(figsize=(11, 6))
        ax.bar(sorted_df["Month"], sorted_df["Revenue"], color='#1abc9c')
        ax.set_title("Months with Highest Revenue (Merge Sort)", fontsize=15)
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue ($)")
        ax.grid(axis='y')
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_least_purchased():
        clear_frame()
        prod_data = df.groupby("Category")["Quantity"].sum().reset_index()
        sorted_data = merge_sort(prod_data.values.tolist(), key=lambda x: x[1], reverse=False)
        sorted_df = pd.DataFrame(sorted_data, columns=["Category", "Quantity"])
        fig, ax = plt.subplots(figsize=(11, 6))
        ax.bar(sorted_df["Category"], sorted_df["Quantity"], color='#e67e22')
        ax.set_title("Products Purchased Least (Merge Sort)", fontsize=15)
        ax.set_xlabel("Product Category")
        ax.set_ylabel("Total Quantity Sold")
        ax.grid(axis='y')
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    btn_frame = tk.Frame(sorted_window, bg="#f9f9f9")
    btn_frame.pack(pady=10)

    btn1 = tk.Button(btn_frame, text="🔼 Show Months with Highest Revenue",
                     bg="#1e90ff", fg="white", font=("Arial", 12, "bold"),
                     width=35, height=2, relief="ridge", command=show_highest_revenue)
    btn2 = tk.Button(btn_frame, text="🔽 Show Products Purchased Least",
                     bg="#ff6347", fg="white", font=("Arial", 12, "bold"),
                     width=35, height=2, relief="ridge", command=show_least_purchased)
    btn1.grid(row=0, column=0, padx=10, pady=5)
    btn2.grid(row=0, column=1, padx=10, pady=5)

# ------------------ CREATE BUTTONS ------------------
line_btn = create_button(sidebar, "📈 Line Chart", "#3498db", show_line_chart)
area_btn = create_button(sidebar, "📉 Area Chart", "#27ae60", show_area_chart)
bar_btn = create_button(sidebar, "📊 Bar Chart", "#f39c12", show_bar_chart)
pie_btn = create_button(sidebar, "🥧 Pie Chart", "#c0392b", show_pie_chart)
sort_btn = create_button(sidebar, "🔍 Merge Sort Insights", "#8e44ad", show_sorted_page)

line_btn.pack(pady=15)
area_btn.pack(pady=15)
bar_btn.pack(pady=15)
pie_btn.pack(pady=15)
sort_btn.pack(pady=15)

# ------------------ RUN APP ------------------
root.mainloop()
