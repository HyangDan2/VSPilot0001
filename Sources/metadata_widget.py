from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QLineEdit, QGroupBox
from typing import Dict, Any


class MetadataWidget(QWidget):
    """메타데이터 입력 위젯"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Metadata Group
        metadata_group = QGroupBox("메타데이터")
        metadata_layout = QVBoxLayout(metadata_group)

        # Steps
        steps_layout = QHBoxLayout()
        steps_layout.addWidget(QLabel("Steps:"))
        self.steps_spin = QSpinBox()
        self.steps_spin.setRange(1, 150)
        self.steps_spin.setValue(20)
        steps_layout.addWidget(self.steps_spin)
        steps_layout.addStretch()
        metadata_layout.addLayout(steps_layout)

        # CFG
        cfg_layout = QHBoxLayout()
        cfg_layout.addWidget(QLabel("CFG:"))
        self.cfg_spin = QDoubleSpinBox()
        self.cfg_spin.setRange(0.1, 30.0)
        self.cfg_spin.setValue(7.0)
        self.cfg_spin.setDecimals(1)
        cfg_layout.addWidget(self.cfg_spin)
        cfg_layout.addStretch()
        metadata_layout.addLayout(cfg_layout)

        # Checkpoint
        ckpt_layout = QHBoxLayout()
        ckpt_layout.addWidget(QLabel("Checkpoint:"))
        self.ckpt_edit = QLineEdit()
        self.ckpt_edit.setPlaceholderText("체크포인트 모델명")
        ckpt_layout.addWidget(self.ckpt_edit)
        metadata_layout.addLayout(ckpt_layout)

        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(64, 2048)
        self.width_spin.setValue(512)
        self.width_spin.setSingleStep(64)
        width_layout.addWidget(self.width_spin)
        width_layout.addStretch()
        metadata_layout.addLayout(width_layout)

        # Height
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(64, 2048)
        self.height_spin.setValue(512)
        self.height_spin.setSingleStep(64)
        height_layout.addWidget(self.height_spin)
        height_layout.addStretch()
        metadata_layout.addLayout(height_layout)

        layout.addWidget(metadata_group)

    def get_metadata(self) -> Dict[str, Any]:
        """메타데이터 반환"""
        return {
            "steps": self.steps_spin.value(),
            "cfg": self.cfg_spin.value(),
            "checkpoint": self.ckpt_edit.text(),
            "width": self.width_spin.value(),
            "height": self.height_spin.value()
        }

    def set_metadata(self, metadata: Dict[str, Any]):
        """메타데이터 설정"""
        self.steps_spin.setValue(metadata.get("steps", 20))
        self.cfg_spin.setValue(metadata.get("cfg", 7.0))
        self.ckpt_edit.setText(metadata.get("checkpoint", ""))
        self.width_spin.setValue(metadata.get("width", 512))
        self.height_spin.setValue(metadata.get("height", 512))