import time
import threading
from typing import Callable

class TimerCore:
    """タイマーの基本機能を管理するクラス"""

    def __init__(self, update_callback: Callable, complete_callback: Callable):
        self.time_left = 0
        self.running = False
        self.update_callback = update_callback
        self.complete_callback = complete_callback
        self._stop_flag = False

    def add_time(self, seconds: int) -> None:
        """時間を追加"""
        self.time_left += seconds
        self.update_callback()

    def start(self) -> None:
        """タイマー開始"""
        if not self.running and self.time_left > 0:
            self.running = True
            self._stop_flag = False
            threading.Thread(target=self._run, daemon=True).start()

    def stop(self) -> None:
        """タイマー停止"""
        self._stop_flag = True
        self.running = False

    def reset(self) -> None:
        """タイマーリセット"""
        self.stop()
        self.time_left = 0
        self.update_callback()

    def _run(self) -> None:
        """タイマーのカウントダウン実行"""
        while not self._stop_flag and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            self.update_callback()

        if self.time_left == 0 and not self._stop_flag:
            self.running = False
            self.complete_callback()