"""
Главная функция
"""

import argparse
from process_audiofile import boost_audio, slow_down_audio

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ускорение аулиофайла")
    parser.add_argument("file", type=str, help="Путь к аудиофайлу")
    parser.add_argument(
        "fuctor", type=float, help="Число, во сколько раз ускорить аудиофайл", default=1
    )
    parser.add_argument(
        "-s",
        "--save",
        type=str,
        help="Путь к директории, куда сохранить ускоренный аудиофайл",
    )
    parser.add_argument(
        "-g", "--graph", type=str, help="Путь к директории, куда сохранить график"
    )
    args = parser.parse_args()
    path_file = args.file
    factor = args.fuctor
    save_path = args.save
    graph_path = args.graph
    if factor > 0:
        boost_audio(path_file, save_path, graph_path, factor)
        print("Программа успешно отработала")
    else:
        slow_down_audio(path_file, save_path, graph_path, abs(factor))
        print("Программа успешно отработала")
