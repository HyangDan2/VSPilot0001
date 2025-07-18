import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QMenuBar, QMenu, QFileDialog, QMessageBox,
    QScrollArea, QComboBox, QSplitter, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QAction

from Sources.image_drop_label import ImageDropLabel
from Sources.metadata_widget import MetadataWidget
from Sources.prompt_widget import PromptWidget
from Sources.data_library import DataLibrary


class ComfyUIPromptViewer(QMainWindow):
    """메인 애플리케이션 클래스"""

    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.data_library = DataLibrary()
        self.image_list = []
        self.current_image_index = -1
        self.setup_ui()
        self.setup_menubar()
        self.load_saved_items()

    def setup_ui(self):
        self.setWindowTitle("ComfyUI Prompt Viewer")
        self.setGeometry(100, 100, 1200, 800)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 스플리터
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        central_widget_layout = QVBoxLayout(central_widget)
        central_widget_layout.addWidget(main_splitter)

        # 좌측 영역 (80% - 이미지)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # 저장된 이미지 드롭다운
        self.saved_combo = QComboBox()
        self.saved_combo.addItem("새 이미지...")
        self.saved_combo.currentTextChanged.connect(self.on_saved_item_selected)
        left_layout.addWidget(self.saved_combo)

        # 이미지 표시 영역
        self.image_label = ImageDropLabel()
        self.image_label.imageDropped.connect(self.load_image)

        # 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.image_label)
        scroll_area.setWidgetResizable(True)
        left_layout.addWidget(scroll_area)

        # 우측 영역 (20% - 메타데이터 및 프롬프트)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # 프롬프트 위젯
        self.prompt_widget = PromptWidget()
        right_layout.addWidget(self.prompt_widget)

        # 메타데이터 위젯
        self.metadata_widget = MetadataWidget()
        right_layout.addWidget(self.metadata_widget)

        # 저장 버튼
        self.save_button = QPushButton("데이터 저장")
        self.save_button.clicked.connect(self.save_data)
        self.save_button.setEnabled(False)
        right_layout.addWidget(self.save_button)

        # 스플리터에 위젯 추가
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)
        main_splitter.setSizes([800, 400])  # 80:20 비율

    def setup_menubar(self):
        menubar = self.menuBar()

        # 파일 메뉴
        file_menu = menubar.addMenu("파일")

        # 이미지 열기
        open_action = QAction("이미지 열기", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        # 데이터 저장
        save_action = QAction("데이터 저장", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        # 종료
        exit_action = QAction("종료", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 보기 메뉴
        view_menu = menubar.addMenu("보기")

        # 저장된 데이터 새로고침
        refresh_action = QAction("새로고침", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.load_saved_items)
        view_menu.addAction(refresh_action)

        # 도움말 메뉴
        help_menu = menubar.addMenu("도움말")

        # 정보
        about_action = QAction("정보", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "이미지 선택", "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path: str):
        """이미지 로드"""
        self.current_image_path = file_path

        # 이미지 리스트에 추가 (중복 방지)
        if file_path not in self.image_list:
            self.image_list.append(file_path)
        self.current_image_index = self.image_list.index(file_path)

        self.display_image(file_path)
        self.save_button.setEnabled(True)

        # 드롭다운을 "새 이미지..."로 설정
        self.saved_combo.setCurrentIndex(0)

    def display_image(self, file_path: str):
        """이미지 표시"""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            # 이미지 크기 조정
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            QMessageBox.warning(self, "오류", "이미지를 로드할 수 없습니다.")

    def save_data(self):
        """데이터 저장"""
        if not self.current_image_path:
            QMessageBox.warning(self, "경고", "저장할 이미지가 없습니다.")
            return

        prompts = self.prompt_widget.get_prompts()
        metadata = self.metadata_widget.get_metadata()

        if not prompts["positive"].strip():
            QMessageBox.warning(self, "경고", "포지티브 프롬프트를 입력하세요.")
            return

        try:
            folder_path = self.data_library.save_data(
                self.current_image_path, prompts, metadata
            )
            QMessageBox.information(self, "성공", f"데이터가 저장되었습니다.\n{folder_path}")
            self.load_saved_items()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 저장 중 오류가 발생했습니다.\n{e}")

    def load_saved_items(self):
        """저장된 아이템 로드"""
        self.saved_combo.clear()
        self.saved_combo.addItem("새 이미지...")

        items = self.data_library.get_saved_items()
        for item in items:
            display_name = f"{item['timestamp']} - {item['folder']}"
            self.saved_combo.addItem(display_name)
            self.saved_combo.setItemData(self.saved_combo.count() - 1, item)

    def on_saved_item_selected(self, text: str):
        """저장된 아이템 선택"""
        if text == "새 이미지...":
            return

        current_index = self.saved_combo.currentIndex()
        if current_index <= 0:
            return

        item = self.saved_combo.itemData(current_index)
        if not item:
            return

        # 데이터 로드
        data = item["data"]
        folder_path = Path(item["path"])
        image_path = folder_path / data["image_file"]

        if image_path.exists():
            self.load_image(str(image_path))
            self.prompt_widget.set_prompts(data["prompts"])
            self.metadata_widget.set_metadata(data["metadata"])

    def show_about(self):
        """정보 표시"""
        QMessageBox.about(
            self, "ComfyUI Prompt Viewer",
            "ComfyUI Prompt Viewer v1.0\n\n"
            "이미지와 프롬프트를 관리하는 도구입니다.\n"
            "PySide6로 제작되었습니다."
        )

    def keyPressEvent(self, event):
        if event.key() == 16777234:  # Left arrow key
            self.navigate_images(-1)  # 이전 이미지
        elif event.key() == 16777236:  # Right arrow key
            self.navigate_images(1)  # 다음 이미지

    def navigate_images(self, direction: int):
        """이미지 목록에서 이전/다음 이미지로 이동"""
        if not self.image_list:
            return

        self.current_image_index += direction
        if self.current_image_index < 0:
            self.current_image_index = 0
        elif self.current_image_index >= len(self.image_list):
            self.current_image_index = len(self.image_list) - 1

        self.current_image_path = self.image_list[self.current_image_index]
        self.display_image(self.current_image_path)
        self.saved_combo.setCurrentIndex(0)