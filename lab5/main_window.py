"""Проигрыватель аудиофайлов"""

import csv
import os
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtMultimedia, QtWidgets

from file_path_iterator import FilePathIterator


class AudioPlayerWindow(QtWidgets.QMainWindow):
    """Главное окно приложения для проигрывания аудиофайлов из датасета."""

    update_progress = QtCore.pyqtSignal(int, int)

    def __init__(self) -> None:
        super().__init__()
        self.current_iterator = None
        self.media_player = QtMultimedia.QMediaPlayer()
        self.current_file_index = 0
        self.total_files = 0
        self.is_playing = False
        self.rows = []

        self.init_ui()
        self.setup_media_player()
        self.setWindowTitle("Аудио датасет - Просмотрщик")
        self.resize(500, 321)

    def init_ui(self) -> None:
        """Инициализация пользовательского интерфейса."""
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)

        file_group = QtWidgets.QGroupBox("Управление датасетом")
        file_layout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()

        self.btn_load_csv = QtWidgets.QPushButton("Загрузить CSV аннотацию")
        self.btn_load_csv.clicked.connect(self.load_csv_file)

        self.btn_load_folder = QtWidgets.QPushButton("Загрузить папку датасета")
        self.btn_load_folder.clicked.connect(self.load_dataset_folder)

        button_layout.addWidget(self.btn_load_csv)
        button_layout.addWidget(self.btn_load_folder)
        button_layout.addStretch()

        self.lbl_current_file = QtWidgets.QLabel("Файл не загружен")
        self.lbl_current_file.setWordWrap(True)

        file_layout.addLayout(button_layout)
        file_layout.addWidget(self.lbl_current_file)
        file_group.setLayout(file_layout)

        info_group = QtWidgets.QGroupBox("Информация о треке")
        info_layout = QtWidgets.QVBoxLayout()

        self.lbl_track_name = QtWidgets.QLabel("Название: --")
        self.lbl_duration = QtWidgets.QLabel("Длительность: --")
        self.lbl_progress = QtWidgets.QLabel("Текущее время: --")

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setTextVisible(False)

        info_layout.addWidget(self.lbl_track_name)
        info_layout.addWidget(self.lbl_duration)
        info_layout.addWidget(self.lbl_progress)
        info_layout.addWidget(self.progress_bar)
        info_group.setLayout(info_layout)

        control_group = QtWidgets.QGroupBox("Управление воспроизведением")
        control_layout = QtWidgets.QHBoxLayout()

        self.btn_prev = QtWidgets.QPushButton("◀ Предыдущий")
        self.btn_prev.clicked.connect(self.play_previous)
        self.btn_prev.setEnabled(False)

        self.btn_play = QtWidgets.QPushButton("▶ Воспроизвести")
        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_play.setEnabled(False)

        self.btn_next = QtWidgets.QPushButton("Следующий ▶")
        self.btn_next.clicked.connect(self.play_next)
        self.btn_next.setEnabled(False)

        self.btn_stop = QtWidgets.QPushButton("■ Стоп")
        self.btn_stop.clicked.connect(self.stop_playback)
        self.btn_stop.setEnabled(False)

        control_layout.addWidget(self.btn_prev)
        control_layout.addStretch()
        control_layout.addWidget(self.btn_play)
        control_layout.addStretch()
        control_layout.addWidget(self.btn_stop)
        control_layout.addStretch()
        control_layout.addWidget(self.btn_next)
        control_group.setLayout(control_layout)

        self.status_label = QtWidgets.QLabel("Готово")
        self.statusBar().addWidget(self.status_label)

        main_layout.addWidget(file_group)
        main_layout.addWidget(info_group)
        main_layout.addWidget(control_group)
        main_layout.addStretch()

        self.setup_styles()

    def setup_styles(self) -> None:
        """Настройка стилей интерфейса."""
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_track_name.setFont(font)
        self.lbl_duration.setFont(font)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(240, 240, 240))
        self.setPalette(palette)

    def setup_media_player(self) -> None:
        """Настройка медиаплеера."""
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.stateChanged.connect(self.on_state_changed)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_progress_display)

    def load_csv_file(self) -> None:
        """Загрузка CSV файла аннотации."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выберите CSV файл аннотации", "", "CSV Files (*.csv)"
        )

        if file_path:
            try:
                self.current_iterator = FilePathIterator(file_path)

                self.rows = self.current_iterator.rows

                self.current_file_index = 0
                self.total_files = len(self.rows)

                self.status_label.setText(f"Загружено файлов: {self.total_files}")

                self.btn_play.setEnabled(self.total_files > 0)
                self.btn_next.setEnabled(self.total_files > 0)
                self.btn_prev.setEnabled(False)
                self.btn_stop.setEnabled(self.total_files > 0)

                if self.total_files > 0:
                    self.load_audio_file(0)
                else:
                    QtWidgets.QMessageBox.warning(
                        self, "Предупреждение", "CSV файл не содержит данных"
                    )

            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Ошибка", f"Не удалось загрузить CSV файл: {str(e)}"
                )

    def load_dataset_folder(self) -> None:
        """Загрузка папки датасета."""
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Выберите папку датасета"
        )

        if folder_path:
            try:
                csv_file = self.create_csv_from_folder(folder_path)
                self.current_iterator = FilePathIterator(csv_file)

                self.rows = self.current_iterator.rows

                self.current_file_index = 0
                self.total_files = len(self.rows)

                self.status_label.setText(
                    f"Загружено файлов из папки: {self.total_files}"
                )

                self.btn_play.setEnabled(self.total_files > 0)
                self.btn_next.setEnabled(self.total_files > 0)
                self.btn_prev.setEnabled(False)
                self.btn_stop.setEnabled(self.total_files > 0)

                if self.total_files > 0:
                    self.load_audio_file(0)
                else:
                    QtWidgets.QMessageBox.warning(
                        self, "Предупреждение", "Папка не содержит аудиофайлов"
                    )

            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, "Ошибка", f"Не удалось загрузить папку: {str(e)}"
                )

    def create_csv_from_folder(self, folder_path: str) -> str:
        """Создает CSV файл на основе аудиофайлов в папке."""
        audio_extensions = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"}

        audio_files = []
        folder = Path(folder_path)

        for ext in audio_extensions:
            audio_files.extend(folder.rglob(f"*{ext}"))

        csv_path = folder / "temp_annotation.csv"

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Filename", "Absolute Path", "Relative Path"]
            )

            for audio_file in audio_files:
                abs_path = str(audio_file.resolve())
                rel_path = str(audio_file.relative_to(folder))
                filename = audio_file.name
                writer.writerow([filename, abs_path, rel_path, "не указана"])

        return str(csv_path)

    def load_audio_file(self, index) -> None:
        """Загрузка аудиофайла по индексу."""
        if not self.rows or index >= len(self.rows):
            return

        self.media_player.stop()

        row = self.rows[index]
        abs_path = row.get("Absolute Path", "")
        rel_path = row.get("Relative Path", "")
        filename = row.get("Filename", "")

        if not abs_path and rel_path:
            abs_path = os.path.join(os.getcwd(), rel_path)

        if abs_path and os.path.exists(abs_path):
            self.media_player.setMedia(
                QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(abs_path))
            )

            track_name = Path(filename).stem if filename else Path(abs_path).stem
            self.lbl_track_name.setText(f"Название: {track_name}")
            self.lbl_current_file.setText(f"Файл: {filename or Path(abs_path).name}")

            self.current_file_index = index
            self.update_navigation_buttons()

            self.status_label.setText(f"Файл {index + 1} из {self.total_files}")

            self.progress_bar.setValue(0)
            self.lbl_progress.setText("Текущее время: 00:00")

        else:
            QtWidgets.QMessageBox.warning(
                self, "Файл не найден", f"Файл не существует: {abs_path}"
            )
            if index + 1 < len(self.rows):
                self.load_audio_file(index + 1)

    def load_next_audio(self) -> None:
        """Загрузка следующего аудиофайла."""
        if self.current_file_index < self.total_files - 1:
            self.load_audio_file(self.current_file_index + 1)
            if self.is_playing:
                self.media_player.play()

    def load_previous_audio(self) -> None:
        """Загрузка предыдущего аудиофайла."""
        if self.current_file_index > 0:
            self.load_audio_file(self.current_file_index - 1)
            if self.is_playing:
                self.media_player.play()

    def toggle_play(self) -> None:
        """Включение/выключение воспроизведения."""
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.btn_play.setText("▶ Воспроизвести")
            self.is_playing = False
            self.timer.stop()
        else:
            self.media_player.play()
            self.btn_play.setText("⏸ Пауза")
            self.is_playing = True
            self.timer.start(50)

    def stop_playback(self) -> None:
        """Остановка воспроизведения."""
        self.media_player.stop()
        self.btn_play.setText("▶ Воспроизвести")
        self.is_playing = False
        self.timer.stop()
        self.progress_bar.setValue(0)
        self.lbl_progress.setText("Текущее время: 00:00")

    def play_next(self) -> None:
        """Воспроизведение следующего трека."""
        self.load_next_audio()

    def play_previous(self) -> None:
        """Воспроизведение предыдущего трека."""
        self.load_previous_audio()

    def update_duration(self, duration: int) -> None:
        """Обновление информации о длительности трека."""
        if duration > 0:
            minutes = duration // 60000
            seconds = (duration % 60000) // 1000
            self.lbl_duration.setText(f"Длительность: {minutes:02d}:{seconds:02d}")

    def update_position(self, position: int) -> None:
        """Обновление текущей позиции воспроизведения."""
        if self.media_player.duration() > 0:
            progress = int((position / self.media_player.duration()) * 100)
            self.progress_bar.setValue(progress)

            minutes = position // 60000
            seconds = (position % 60000) // 1000
            self.lbl_progress.setText(f"Текущее время: {minutes:02d}:{seconds:02d}")

    def update_progress_display(self) -> None:
        """Обновление отображения прогресса через таймер."""
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            position = self.media_player.position()
            self.update_position(position)

    def on_state_changed(self, state) -> None:
        """Обработка изменения состояния медиаплеера."""
        if state == QtMultimedia.QMediaPlayer.StoppedState:
            self.timer.stop()
            self.btn_play.setText("▶ Воспроизвести")
            self.is_playing = False

            if (
                self.media_player.position() >= self.media_player.duration() - 100
                and self.current_file_index < self.total_files - 1
            ):
                QtCore.QTimer.singleShot(500, self.play_next)

    def update_navigation_buttons(self) -> None:
        """Обновление состояния кнопок навигации."""
        self.btn_prev.setEnabled(self.current_file_index > 0)
        self.btn_next.setEnabled(self.current_file_index < self.total_files - 1)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Обработка закрытия окна."""
        self.media_player.stop()
        event.accept()


def main():
    """Главная функция"""
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Аудио датасет - Просмотрщик")

    window = AudioPlayerWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
