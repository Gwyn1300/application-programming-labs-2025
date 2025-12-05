import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

def reduce_array(arr, factor) -> np.array:
    """
    Уменьшает массив 'arr' в 'factor' раз путем усреднения групп элементов.
    :arr: Входной массив
    :factor: Во сколько раз уменьшить массив
    """
    new_len = int(len(arr) / factor)
    result = np.zeros(new_len) if len(arr.shape) == 1 else np.zeros((new_len, arr.shape[1]))
    
    for i in range(new_len):
        start = int(i * factor)
        end = int((i + 1) * factor)
        if len(arr.shape) == 1:
            result[i] = np.mean(arr[start:end])
        else:
            result[i] = np.mean(arr[start:end], axis=0)
    
    return result

def create_comparison_charts(original_count, reduced_count, factor, samplerate):
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
    
    #график сравнения размеров массивов
    labels_size = ['Исходный массив', f'Уменьшенный массив\n(в {factor:.1f} раза)']
    counts = [original_count, reduced_count]
    colors = ['blue', 'red']
    
    bars1 = ax1.bar(labels_size, counts, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    ax1.set_ylabel('Количество элементов', fontsize=12)
    ax1.set_title('Сравнение размеров массивов', fontsize=14, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3, axis='y')
    
    max_count = max(counts)
    ax1.set_ylim(0, max_count * 1.15)
    
    for bar, count in zip(bars1, counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height + max_count * 0.02,
                f'{count:,}\nэлементов', ha='center', va='bottom', fontsize=11,
                fontweight='bold')
    
    # график сравнения длительности аудио
    labels_duration = ['Исходное аудио', f'Ускоренное аудио\n(в {factor:.1f} раза)']
    durations = [duration_original, duration_reduced]
    colors_duration = ['green', 'orange']
    
    bars2 = ax2.bar(labels_duration, durations, color=colors_duration, alpha=0.7, 
                   edgecolor='black', linewidth=2)
    
    ax2.set_ylabel('Длительность (секунды)', fontsize=12)
    ax2.set_title('Сравнение длительности аудио', fontsize=14, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, axis='y')
    
    def format_duration(seconds):
        if seconds >= 60:
            minutes = seconds // 60
            return f'{int(minutes)} мин {int(seconds % 60)} сек'
        else:
            return f'{int(seconds)} сек'
    
    max_duration = max(durations)
    ax2.set_ylim(0, max_duration * 1.15)
    

    for bar, duration in zip(bars2, durations):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + max_duration * 0.02,
                f'{format_duration(duration)}', ha='center', va='bottom', fontsize=11,
                fontweight='bold')
    
    fig.suptitle(f'Анализ аудиофайла: размер массива и длительность', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0.08, 1, 0.95]) 
    return fig, (ax1, ax2)

if __name__ == "__main__":
    
    data, samplerate = sf.read(r"C:\\don't system\\study\\application_programming\\application-programming-labs-2025\\lab3\\harp.0.mp3")

    print(f"Массив сэмплов: {data}")
    print(f"Частота дискретизации: {samplerate}")

    original_count = len(data)

    factor = float(input("Введите во сколько раз уменьшить массив: "))
    data_reduced = reduce_array(data, factor)

    reduced_count = len(data_reduced)   

    fig, axes = create_comparison_charts(original_count, reduced_count, factor, samplerate)
    
    
    plt.savefig('audio_comparison_charts.png', dpi=150, bbox_inches='tight')
    print("График сохранен как 'audio_comparison_charts.png'")
    
    sf.write(r"C:\\don't system\\study\\application_programming\\application-programming-labs-2025\\lab3\\new_audio.mp3", data, samplerate)
    plt.show()