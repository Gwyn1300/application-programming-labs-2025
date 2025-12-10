"""
Создание графика распределения аудиофайлов по диапазонам размаха амплитуды
"""

import matplotlib.pyplot as plt


def creat_graph(range_counts, save_path):
    """Создает график распределения аудиофайлов по диапазонам размаха амплитуды
    :range_counts: Series с количеством файлов в каждом диапазоне.
    :save_path: Путь к директории для сохранения графика
    """
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        range_counts.index, range_counts.values, color="skyblue", edgecolor="black"
    )
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.1,
            f"{int(height)}",
            ha="center",
            va="bottom",
        )
    plt.title(
        "Распределение аудиофайлов по диапазонам размаха амплитуды",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Диапазон размаха амплитуды", fontsize=12)
    plt.ylabel("Количество файлов", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    output_plot = save_path + r"\amplitude_range_histogram.png"
    plt.savefig(output_plot, dpi=300, bbox_inches="tight")
    print(f"График сохранен в файл: {output_plot}")
