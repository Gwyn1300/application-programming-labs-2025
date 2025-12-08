"""
Файл для работы с графиками
"""

import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def create_comparison_charts(
    original_count, reduced_count, factor, samplerate
) -> Figure:
    """
    Создает два графика: сравнение размеров массивов и сравнение длительности аудио
    :original_count: Количество элементов в исходном массиве
    :reduced_count: Количество элементов в уменьшенном массиве
    :factor: Во сколько раз уменьшен массив
    :samplerate: Частота дискретизации аудио
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    duration_original = original_count / samplerate
    duration_reduced = reduced_count / samplerate

    # график сравнения размеров массивов
    labels_size = ["Исходный массив", f"Уменьшенный массив\n(в {factor:.1f} раза)"]
    counts = [original_count, reduced_count]
    colors = ["blue", "red"]

    bars1 = ax1.bar(
        labels_size, counts, color=colors, alpha=0.7, edgecolor="black", linewidth=2
    )

    ax1.set_ylabel("Количество элементов", fontsize=12)
    ax1.set_title("Сравнение размеров массивов", fontsize=14, fontweight="bold", pad=20)
    ax1.grid(True, alpha=0.3, axis="y")

    max_count = max(counts)
    ax1.set_ylim(0, max_count * 1.15)

    for bar_plot, count in zip(bars1, counts):
        height = bar_plot.get_height()
        ax1.text(
            bar_plot.get_x() + bar_plot.get_width() / 2,
            height + max_count * 0.02,
            f"{count:,}\nэлементов",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    # график сравнения длительности аудио
    labels_duration = ["Исходное аудио", f"Ускоренное аудио\n(в {factor:.1f} раза)"]
    durations = [duration_original, duration_reduced]
    colors_duration = ["green", "orange"]

    bars2 = ax2.bar(
        labels_duration,
        durations,
        color=colors_duration,
        alpha=0.7,
        edgecolor="black",
        linewidth=2,
    )

    ax2.set_ylabel("Длительность (секунды)", fontsize=12)
    ax2.set_title(
        "Сравнение длительности аудио", fontsize=14, fontweight="bold", pad=20
    )
    ax2.grid(True, alpha=0.3, axis="y")

    def format_duration(seconds):
        if seconds >= 60:
            minutes = seconds // 60
            return f"{int(minutes)} мин {int(seconds % 60)} сек"
        else:
            return f"{int(seconds)} сек"

    max_duration = max(durations)
    ax2.set_ylim(0, max_duration * 1.15)

    for bar_plot, duration in zip(bars2, durations):
        height = bar_plot.get_height()
        ax2.text(
            bar_plot.get_x() + bar_plot.get_width() / 2,
            height + max_duration * 0.02,
            f"{format_duration(duration)}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    fig.suptitle(
        "Анализ аудиофайла: размер массива и длительность",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    return fig


def save_graph(
    fig: Figure,
    path: str,
) -> bool:
    """
    Сохраняет график по заданному пути"""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fig.savefig(
            path + "\\audio_comparison_charts.png", dpi=150, bbox_inches="tight"
        )
        print(f"Файл успешно создан: {path+"\\audio_comparison_charts.png"}")
        return True
    except FileNotFoundError:
        print(f"Ошибка: директория не найдена для пути '{path}'")
        return False
    except OSError as e:
        print(f"Ошибка при записи файла '{path+"\\audio_comparison_charts.png"}': {e}")
    return False
