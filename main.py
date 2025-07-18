import sys
from PySide6.QtWidgets import QApplication
from Sources.main_window import ComfyUIPromptViewer


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 모던한 스타일

    window = ComfyUIPromptViewer()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()