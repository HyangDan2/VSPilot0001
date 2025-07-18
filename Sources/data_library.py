import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class DataLibrary:
    """데이터 라이브러리 클래스"""

    def __init__(self, data_dir: str = "Data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.log_file = self.data_dir / "library.log"

    def save_data(self, image_path: str, prompts: Dict[str, str],
                  metadata: Dict[str, Any]) -> str:
        """데이터 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"img_{timestamp}"
        folder_path = self.data_dir / folder_name
        folder_path.mkdir(exist_ok=True)

        # 이미지 복사
        image_ext = Path(image_path).suffix
        new_image_path = folder_path / f"image{image_ext}"
        shutil.copy2(image_path, new_image_path)

        # 메타데이터 저장
        data = {
            "timestamp": timestamp,
            "prompts": prompts,
            "metadata": metadata,
            "image_file": f"image{image_ext}"
        }

        json_path = folder_path / "data.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 로그 기록
        self._log_action(f"Saved data to {folder_name}")

        return str(folder_path)

    def load_data(self, folder_path: str) -> Optional[Dict[str, Any]]:
        """데이터 로드"""
        json_path = Path(folder_path) / "data.json"
        if not json_path.exists():
            return None

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            self._log_action(f"Error loading data from {folder_path}: {e}")
            return None

    def get_saved_items(self) -> list:
        """저장된 아이템 목록 반환"""
        items = []
        for folder_path in self.data_dir.iterdir():
            if folder_path.is_dir() and folder_path.name.startswith("img_"):
                data = self.load_data(str(folder_path))
                if data:
                    items.append({
                        "folder": folder_path.name,
                        "path": str(folder_path),
                        "timestamp": data.get("timestamp", ""),
                        "data": data
                    })
        return sorted(items, key=lambda x: x["timestamp"], reverse=True)

    def _log_action(self, message: str):
        """로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message)