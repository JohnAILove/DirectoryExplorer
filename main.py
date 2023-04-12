import os
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar

# browse_folder函數是一個打開文件夾瀏覽器的函數，並將選擇的文件夾路徑顯示在文字框中。
def browse_folder():
    folder_path = filedialog.askdirectory()
    path_var.set(folder_path)

# browse_output_file函數是一個打開檔案儲存對話框的函數，並將選擇的檔案位置顯示在文字框中。
def browse_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    output_var.set(output_file)

# add_to_ignore_list函數是一個將文字框中的文字添加到忽略文件夾列表框中的函數。
def add_to_ignore_list():
    item = ignore_var.get()
    ignore_listbox.insert(tk.END, item)
    ignore_var.set("")

# add_to_extension_list函數是一個將文字框中的文字添加到忽略副檔名列表框中的函數。
def add_to_extension_list():
    item = extension_var.get()
    extension_listbox.insert(tk.END, item)
    extension_var.set("")

# analyze_folder函數是一個分析文件夾的核心函數。它會遍歷文件夾的每個文件和子文件夾，並根據指定的忽略條件將文件夾樹狀結構寫入文字檔。
def analyze_folder():
    folder_path = path_var.get()
    ignored_folders = set(ignore_listbox.get(0, tk.END))
    ignored_extensions = set(extension_listbox.get(0, tk.END))
    output_file = output_var.get()

    # tree_walk函數是一個遍歷文件夾樹狀結構的輔助函數。
    def tree_walk(path, depth=0):
        # 遍歷當前文件夾中的所有文件和子文件夾
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            # 如果當前的文件是一個文件夾且不在忽略文件夾列表中，則將其進一步遍歷。
            if os.path.isdir(full_path) and entry not in ignored_folders:
                output.write(f"{'│   ' * (depth - 1)}{'├─ ' if depth > 0 else ''}{entry}/\n")
                tree_walk(full_path, depth + 1)
            # 如果當前文件是一個檔案且其副檔名不在忽略副檔名列表中，則將其寫入文字檔。
            elif os.path.isfile(full_path) and not any(full_path.endswith(ext) for ext in ignored_extensions):
                output.write(f"{'│   ' * (depth - 1)}{'├─ ' if depth > 0 else ''}{entry}\n")

    # 使用with open語句以寫入模式打開文字檔，並使用tree_walk函數將文件夾樹狀結構寫入文字檔。
    with open(output_file, "w") as output:
        tree_walk(folder_path)

    # 使用with open語句以讀取模式打開文字檔，並將其內容讀取到變數content中。
    with open(output_file, "r") as output:
        content = output.read()
        # 將文字檔內容顯示在結果文字區域中。
        result.delete(1.0, tk.END)
        result.insert(tk.END, content)

app = tk.Tk()  # 建立Tkinter應用程式實例

app.title("文件夾分析器")  # 設定應用程式的標題

# 初始化各種變數
path_var = tk.StringVar()
output_var = tk.StringVar()
ignore_var = tk.StringVar()
extension_var = tk.StringVar()

# 建立標籤、輸入框和按鈕，以選擇文件夾
tk.Label(app, text="選擇文件夾:").grid(row=0, column=0, sticky="w")
tk.Entry(app, textvariable=path_var).grid(row=0, column=1)
tk.Button(app, text="瀏覽", command=browse_folder).grid(row=0, column=2)

# 建立標籤、輸入框和按鈕，以選擇輸出文件位置
tk.Label(app, text="輸出文件位置:").grid(row=1, column=0, sticky="w")
tk.Entry(app, textvariable=output_var).grid(row=1, column=1)
tk.Button(app, text="瀏覽", command=browse_output_file).grid(row=1, column=2)

# 建立標籤、輸入框和按鈕，以新增要忽略的文件夾
tk.Label(app, text="忽略文件夾:").grid(row=2, column=0, sticky="w")
tk.Entry(app, textvariable=ignore_var).grid(row=2, column=1)
tk.Button(app, text="新增", command=add_to_ignore_list).grid(row=2, column=2)

# 建立列表框，顯示要忽略的文件夾
ignore_listbox = Listbox(app)
ignore_listbox.grid(row=3, column=1, pady=10)

# 建立標籤、輸入框和按鈕，以新增要忽略的副檔名
tk.Label(app, text="忽略副檔名:").grid(row=4, column=0, sticky="w")
tk.Entry(app, textvariable=extension_var).grid(row=4, column=1)
tk.Button(app, text="新增", command=add_to_extension_list).grid(row=4, column=2)

# 建立列表框，顯示要忽略的副檔名
extension_listbox = Listbox(app)
extension_listbox.grid(row=5, column=1, pady=10)

# 建立文字框，顯示分析結果
result = tk.Text(app, wrap=tk.WORD)
result.grid(row=6, column=0, columnspan=3)

# 建立滾動條，與文字框關聯
scrollbar = Scrollbar(app, command=result.yview)
scrollbar.grid(row=6, column=3, sticky="ns")
result.config(yscrollcommand=scrollbar.set)

# 建立按鈕，以觸發文件夾分析功能
analyze_button = tk.Button(app, text="分析文件夾", command=analyze_folder)
analyze_button.grid(row=7, column=1, pady=10)

# 啟動應用程式主循環
app.mainloop()