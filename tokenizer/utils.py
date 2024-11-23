import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
import pandas as pd
import numpy as np
import spacy_tokenizer


def drawWordCloud(file_path: str):
    data = []
    with open(file_path, "r") as file:
        data = json.load(file)
    word_freq = {item["word"]: item["count"] for item in data}
    # 生成词云
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(word_freq)

    # 显示生成的词云
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def drawYearDistribution(file_path: str):
    df = pd.read_csv(file_path)
    df["time"] = pd.to_datetime(df["publish_time"], format="mixed")
    # 提取年份
    df["year"] = df["time"].dt.year
    # 统计每个年份的数量
    year_counts = df["year"].value_counts().sort_index()
    # 绘图
    figure, ax1 = plt.subplots()
    ax1.bar(year_counts.index, year_counts.values, color="b")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Count")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    # 添加折线图
    ax2 = ax1.twinx()
    ax2.plot(year_counts.index, year_counts.values, color="r", marker="o", markersize=3)
    ax2.set_ylim(ax1.get_ylim())
    plt.title("Publication date distribution of the papers")
    plt.show()


def drawJournalDistribution(file_path: str):
    df = pd.read_csv(file_path)
    journal_counts = df["journal"].value_counts().sort_index()

    if len(journal_counts) > 10:
        top_10 = journal_counts.nlargest(10)
        others = journal_counts.iloc[10:].sum()
        journal_counts = pd.concat([top_10, pd.Series([others], index=["Others"])])

    # 画Donut Chart
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        journal_counts,
        labels=journal_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops=dict(width=0.3),
    )

    # 标注数量和百分比
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        x = wedge.r * 0.9 * np.cos(np.deg2rad(angle))
        y = wedge.r * 0.9 * np.sin(np.deg2rad(angle))
        ax.text(x, y, f"{journal_counts.values[i]}", ha="center", va="center")
    plt.title("The journal distribution of the papers")
    plt.show()


def drawLanguageDistribution(directory_path: str):
    """
    directory_path: A complete directory of proceedings for loading all papers and identifying the language of the papers
    """
    tokenizer = spacy_tokenizer.SpacyTokenizer()
    tokenizer.set_directory_path(directory_path)
    paper_language = tokenizer.get_paper_language()
    language_count = (
        paper_language["language"].value_counts().sort_values(ascending=False)
    )
    figure, ax1 = plt.subplots()
    ax1.bar(language_count.index, language_count.values, color="b")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Count")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    plt.title("Language distribution of the papers")
    plt.show()

    # 不包含英语的donut图
    language_count = language_count[language_count.index != "en"]
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        language_count,
        labels=language_count.index,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops=dict(width=0.3),
    )
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1
        x = wedge.r * 0.9 * np.cos(np.deg2rad(angle))
        y = wedge.r * 0.9 * np.sin(np.deg2rad(angle))
        ax.text(x, y, f"{language_count.values[i]}", ha="center", va="center")
    plt.title("Language(without English) distribution of the papers")
    plt.show()
