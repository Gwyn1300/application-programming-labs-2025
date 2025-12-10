"""
Работа с аудиофайлами: вычисление размаха амплитуды, создание DataFrame и графиков.
"""

import pandas as pd
import numpy as np
import soundfile as sf
from graph import creat_graph


def calculate_amplitude_range(file_path) -> float:
    """
    Вычисляет размах амплитуды (max-min) аудиофайла
    :file_path: Путь к аудиофайлу.
    """
    try:
        data = sf.read(file_path)[0]
        if data.ndim > 1:
            data = data.mean(axis=1)
            amp_range = np.max(data) - np.min(data)
            return amp_range
    except (FileNotFoundError, OSError) as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return None


def create_range_label(value, amplitude_ranges) -> str:
    """
    Создает метку диапазона для значения размаха амплитуды
    :value: Значение размаха амплитуды.
    :amplitude_ranges: Список диапазонов амплитуды.
    """
    if pd.isna(value):
        return "Ошибка чтения"
    valid_values = [v for v in amplitude_ranges if not pd.isna(v)]
    if not valid_values:
        return "Нет данных"
    min_val = min(valid_values)
    max_val = max(valid_values)
    num_bins = 7
    bin_edges = np.linspace(min_val, max_val + 0.01, num_bins + 1)
    for i in range(len(bin_edges) - 1):
        if bin_edges[i] <= value < bin_edges[i + 1]:
            return f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}"
    return f"{bin_edges[-2]:.2f}-{bin_edges[-1]:.2f}"


def sort_by_amplitude_range(df) -> pd.DataFrame:
    """
    Сортирует DataFrame по диапазону амплитуды
    :df: DataFrame с колонкой "_amplitude_range_numeric
    """
    sorted_df = df.sort_values("_amplitude_range_numeric", ascending=True)
    return sorted_df.drop(columns=["_amplitude_range_numeric"])


def filter_by_amplitude_range(df, target_range) -> pd.DataFrame:
    """
    Фильтрует DataFrame по конкретному диапазону амплитуды
    :df: DataFrame с колонкой "Amplitude range
    :target_range: Целевой диапазон амплитуды
    """
    filtered_df = df[df["Amplitude range"] == target_range]
    return filtered_df.drop(columns=["_amplitude_range_numeric"])


def create_dataframe(csv_path, save_path) -> None:
    """
    Создает DataFrame из CSV-файла, вычисляет размах амплитуды и строит график
    :csv_path: Путь к CSV-файлу с аннотацией.
    :save_path: Путь к директории для сохранения обработанных данных
    """
    df = pd.read_csv(csv_path)
    df = df[["Absolute Path", "Relative Path"]]
    print("Вычисление размаха амплитуды для аудиофайлов...")
    amplitude_ranges = df["Absolute Path"].apply(calculate_amplitude_range)
    df["Amplitude range"] = [
        create_range_label(val, amplitude_ranges) for val in amplitude_ranges
    ]
    df["_amplitude_range_numeric"] = amplitude_ranges
    sorted_df = sort_by_amplitude_range(df)
    output_df = df.drop(columns=["_amplitude_range_numeric"])
    output_csv = "audio_files_with_amplitude.csv"
    output_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"DataFrame сохранен в файл: {output_csv}")
    range_counts = sorted_df["Amplitude range"].value_counts().sort_index()
    creat_graph(range_counts, save_path)
