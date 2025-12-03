import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

def reduce_array(arr, factor):
    """
    Уменьшает массив 'arr' в 'factor' раз путем усреднения групп элементов.
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

