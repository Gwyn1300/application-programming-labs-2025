'''
Главный файл для запуска
'''
import argparse
from dataframe import create_dataframe

def main():
    '''
    Главная функция для обработки данных пользователей
    '''
    parser = argparse.ArgumentParser(description="Обработка данных пользователей")
    parser.add_argument(
        "annotation", type=str, help="Путь к файлу аннотоции"
    )
    parser.add_argument(
        "save_path", type=str, help="Путь к дериктории для сохранения обработанных данных"
    )
    args = parser.parse_args()
    csv_path = args.annotation
    save_path = args.save_path
    create_dataframe(csv_path, save_path)

if __name__ == "__main__":
    main()
