# %%
import spacy_tokenizer

if __name__ == "__main__":
    directory_path = "../../Partial/pdf_json"
    tokenizer = spacy_tokenizer.SpacyTokenizer()
    tokenizer.set_directory_path(directory_path)
    tokenizer.load_stop_words("../../Partial/stopwords.txt")
    tokenizer.run()


# %%
import utils

# draw word cloud figure
file_path = "../../Partial/pdf_json/results/result/top50.json"
utils.drawWordCloud(file_path=file_path)
# draw papers' year distribution figure
file_path = "../../Partial/meta_10k.csv"
utils.drawYearDistribution(file_path=file_path)
# draw papers' journal distribution figure
file_path = "../../Partial/meta_10k.csv"
utils.drawJournalDistribution(file_path=file_path)
# draw papers' language distribution figure
directory_path = "../../Partial/pdf_json"
utils.drawLanguageDistribution(directory_path=directory_path)

# %%
import pandas as pd
import tkinter as tk
from tkinter import ttk
import glob
import json
import paper_schema

df = pd.read_json("../../Partial/inverted.json")
# 创建一个可视化窗口
root = tk.Tk()
root.title("Keyword Search")

# 创建输入框和标签
label = tk.Label(root, text="Keyword")
label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)


# 加载所有文件，获取PDF sha1值和paper title
def get_paper_titles(directory_path: str):
    paper_search_dic: dict[str, str] = dict()
    dir = directory_path + "/*.json"
    files = glob.glob(dir)
    for file_path in files:
        with open(file_path, "r") as file:
            data = json.load(file)
            paper = paper_schema.PaperSchema(**data)
            paper_search_dic.update({paper.paper_id: paper.metadata.title})
    return paper_search_dic


# 根据sha1搜索paper的title
file_title_dic = get_paper_titles("../../Partial/pdf_json")


# 定义搜索函数
def search_keyword():
    keyword = entry.get()
    if keyword in df["word"].values:
        file_count_list = df.loc[df["word"] == keyword, "fileCount"].values[0]
        for item in file_count_list:
            item["file"] = item["file"].replace(".json", "")
            item["title"] = file_title_dic.get(item["file"], "Unknown Title")
        file_count_df = pd.DataFrame(file_count_list)
        update_treeview(file_count_df)
    else:
        result_label.config(text="Keyword not found")


# 更新Treeview内容
def update_treeview(data):
    for item in tree.get_children():
        tree.delete(item)
    for index, row in data.iterrows():
        tree.insert("", tk.END, values=(row["file"], row["title"], row["count"]))


# 创建确认按钮
button = tk.Button(root, text="Confirm", command=search_keyword)
button.pack(pady=5)

# 创建Treeview来显示搜索结果
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
tree.pack()

tree_scroll.config(command=tree.yview)

tree["columns"] = ("File", "Title", "Count")
tree.column("#0", width=0, stretch=tk.NO)
tree.column("File", anchor=tk.W, width=300)
tree.column("Title", anchor=tk.W, width=600)
tree.column("Count", anchor=tk.CENTER, width=100)

tree.heading("#0", text="", anchor=tk.W)
tree.heading("File", text="File", anchor=tk.W)
tree.heading("Title", text="Title", anchor=tk.W)
tree.heading("Count", text="Count", anchor=tk.CENTER)

# 运行窗口主循环
root.mainloop()
# %%
