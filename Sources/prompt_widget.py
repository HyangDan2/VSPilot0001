from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QGroupBox
from typing import Dict


class PromptWidget(QWidget):
    """프롬프트 입력 위젯"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Positive Prompt
        pos_group = QGroupBox("Positive Prompt")
        pos_layout = QVBoxLayout(pos_group)
        self.positive_edit = QTextEdit()
        self.positive_edit.setPlaceholderText("포지티브 프롬프트를 입력하세요...")
        self.positive_edit.setMaximumHeight(150)
        pos_layout.addWidget(self.positive_edit)
        layout.addWidget(pos_group)

        # Negative Prompt
        neg_group = QGroupBox("Negative Prompt")
        neg_layout = QVBoxLayout(neg_group)
        self.negative_edit = QTextEdit()
        self.negative_edit.setPlaceholderText("네거티브 프롬프트를 입력하세요...")
        self.negative_edit.setMaximumHeight(150)
        neg_layout.addWidget(self.negative_edit)
        layout.addWidget(neg_group)

    def get_prompts(self) -> Dict[str, str]:
        """프롬프트 반환"""
        return {
            "positive": self.positive_edit.toPlainText(),
            "negative": self.negative_edit.toPlainText()
        }

    def set_prompts(self, prompts: Dict[str, str]):
        """프롬프트 설정"""
        self.positive_edit.setText(prompts.get("positive", ""))
        self.negative_edit.setText(prompts.get("negative", ""))