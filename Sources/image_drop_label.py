from PySide6.QtWidgets import QLabel, QFileDialog
from PySide6.QtCore import Qt, QMimeData, QUrl, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class ImageDropLabel(QLabel):
    """드래그 앤 드롭을 지원하는 이미지 라벨"""
    imageDropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f0f0f0;
                text-align: center;
                color: #666;
                font-size: 14px;
            }
            QLabel:hover {
                border-color: #007acc;
                background-color: #e6f3ff;
            }
        """)
        self.setText("이미지를 드래그하여 놓으세요\n또는 클릭하여 선택하세요")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(400, 300)
        self.setScaledContents(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].isLocalFile():
                file_path = urls[0].toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            file_path = urls[0].toLocalFile()
            self.imageDropped.emit(file_path)
            event.acceptProposedAction()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: 
            file_path, _ = QFileDialog.getOpenFileName(
                self, "이미지 선택", "",
                "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
            )
            if file_path:
                self.imageDropped.emit(file_path)