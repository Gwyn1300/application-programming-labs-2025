"""
Обработка аудиофайлов
"""

import numpy as np
import soundfile as sf
from graph import create_comparison_charts, save_graph


def read_file(path: str):
    """
    Считывает аудиофайл
    :path:путь к файлу
    Returns:
        tuple or None:
            - Если успешно: (np.ndarray, int)
            - Если ошибка: None
    """
    try:
        data, samplerate = sf.read(path)
        return data, samplerate
    except FileNotFoundError:
        print(f"Файл {path} не найден")
        return None
    except OSError as e:
        print(f"Ошибка чтения файла '{path}': {e}")
        return None


def save_file(path: str, data: np.array, samplerate: any) -> bool:
    """
    Сохраняет файл
    :path: путь к дериктории, в которой нужно сохранить файл
    :data: массив сэмплов
    :samplerate: частота дискретизации
    """
    try:
        sf.write(path + "\\new_file.mp3", data, samplerate)
        return True
    except FileNotFoundError:
        print(f"Ошибка: директория не найдена для пути '{path}'")
        return False
    except OSError as e:
        print(f"Ошибка при записи файла '{path+"\\audio_comparison_charts.png"}': {e}")
    return False


def reduce_array(arr: np.array, factor: float) -> np.array:
    """
    Уменьшает массив 'arr' в 'factor' раз
    :arr: Входной массив
    :factor: во сколько раз уменьшить массив
    """
    new_len = int(len(arr) / factor)
    result = (
        np.zeros(new_len) if len(arr.shape) == 1 else np.zeros((new_len, arr.shape[1]))
    )

    for i in range(new_len):
        start = int(i * factor)
        end = int((i + 1) * factor)
        if len(arr.shape) == 1:
            result[i] = np.mean(arr[start:end])
        else:
            result[i] = np.mean(arr[start:end], axis=0)

    return result


def print_info_audio(data: np.array, samplerate: any):
    """
    Вывод данных аудиофайла
    :data: массив сэмплов
    :samplerate: частота дискретизации
    """
    try:
        print(f"Размер аудиофайла: {len(data)}")
        print(f"Частота дискретизации: {samplerate}")
    except (TypeError, ValueError) as e:
        print(f"Ошибка форматирования данных: {e}")
    except OSError as e:
        print(f"Ошибка ввода-вывода: {e}")


def boost_audio(path_file, save_path, graph_path: str, factor: float):
    """
    Ускорение аудиофайла
    :path_file: путь к аудиофайлу
    :save_path: путь к директории, куда сохранить ускоренный аудиофайл
    :graph_path: путь к директории, куда сохранить график
    :factor: число, во сколько раз ускорить аудиофайл
    """
    data, samplerate = read_file(path_file)
    data_reduced = reduce_array(data, factor)
    reduced_count = len(data_reduced)
    original_count = len(data)
    print_info_audio(data, samplerate)
    fig = create_comparison_charts(original_count, reduced_count, factor, samplerate)
    save_graph(fig, graph_path)
    save_file(save_path, data_reduced, samplerate)


def slow_down_audio(path_file, save_path, graph_path: str, factor: float):
    """
    Замедление аудиофайла
    :path_file: путь к аудиофайлу
    :save_path: путь к директории, куда сохранить ускоренный аудиофайл
    :graph_path: путь к директории, куда сохранить график
    :factor: число, во сколько раз ускорить аудиофайл
    """
    data, samplerate = read_file(path_file)
    data_slowed = increase_array(data, factor)
    slowed_count = len(data_slowed)
    original_count = len(data)
    print_info_audio(data, samplerate)
    fig = create_comparison_charts(original_count, slowed_count, factor, samplerate)
    save_graph(fig, graph_path)
    save_file(save_path, data_slowed, samplerate)


def increase_array(data, factor):
    """
    Увеличение массива

    data: аудио данные (моно или стерео)
    factor: во сколько раз замедлить
    """
    original_length = data.shape[0]
    new_length = int(original_length * factor)
    original_indices = np.arange(original_length)
    new_indices = np.linspace(0, original_length - 1, new_length)
    if len(data.shape) == 1:
        slowed_audio = np.interp(new_indices, original_indices, data)
    else:
        slowed_audio = np.zeros((new_length, data.shape[1]))
        for channel in range(data.shape[1]):
            slowed_audio[:, channel] = np.interp(
                new_indices, original_indices, data[:, channel]
            )
    return slowed_audio
