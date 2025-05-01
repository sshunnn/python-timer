import tkinter as tk
from tkinter import messagebox
from config.styles import Styles
from core.timer import TimerCore

class TimerWidget:
    """単一のタイマーウィジェット"""

    # ボタン定義
    BUTTONS = [
        {"text": "+1分", "command": "add_time", "args": 60, "row": 2, "column": 0},
        {"text": "+1時間", "command": "add_time", "args": 3600, "row": 2, "column": 1},
        {"text": "スタート", "command": "start", "needs_args": False, "row": 3, "column": 0},
        {"text": "ストップ", "command": "stop", "needs_args": False, "row": 3, "column": 1},
        {"text": "リセット", "command": "reset", "needs_args": False, "row": 4, "column": 0, "columnspan": 2}
    ]

    def __init__(self, parent: tk.Frame, name: str):
        self.parent = parent
        self.name = name
        self.buttons = {}
        
        # タイマーコアの初期化
        self.timer = TimerCore(
            update_callback=self.update_timer_label,
            complete_callback=self.on_timer_complete
        )
        
        self._create_widgets()
        self._setup_layout()
        self._update_button_states()

    def _create_widgets(self):
        """UIコンポーネントの作成"""
        # メインフレーム
        self.frame = tk.Frame(
            self.parent,
            bg=Styles.COLORS["frame_bg"],
            relief="ridge",
            borderwidth=1
        )

        # 左側のフレーム（タイマー部分）
        self.timer_frame = tk.Frame(
            self.frame,
            bg=Styles.COLORS["frame_bg"]
        )

        self.name_label = tk.Label(
            self.timer_frame,
            text=self.name,
            font=Styles.FONTS["title"],
            bg=Styles.COLORS["frame_bg"],
            fg=Styles.COLORS["title"]
        )

        self.timer_label = tk.Label(
            self.timer_frame,
            text="00:00:00",
            font=Styles.FONTS["time"],
            bg=Styles.COLORS["frame_bg"],
            fg=Styles.COLORS["time"]
        )

        # 右側のフレーム（メモ部分）
        self.memo_frame = tk.Frame(
            self.frame,
            bg=Styles.COLORS["frame_bg"]
        )

        # メモのラベルを追加
        self.memo_label = tk.Label(
            self.memo_frame,
            text="メモ",
            font=Styles.FONTS["memo"],
            bg=Styles.COLORS["frame_bg"],
            fg=Styles.COLORS["text"]
        )

        self.memo = tk.Text(
            self.memo_frame,
            height=Styles.SIZES["memo_height"],
            font=Styles.FONTS["memo"],
            bg=Styles.COLORS["memo_bg"],
            wrap=tk.WORD
        )

        self._create_buttons()

    def _setup_layout(self):
        """レイアウトの設定"""
        self.frame.pack(pady=10, padx=10, fill=tk.X)
        
        # 左側のタイマー部分
        self.timer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.name_label.grid(row=0, column=0, columnspan=2, pady=(5, 0))
        self.timer_label.grid(row=1, column=0, columnspan=2, pady=(5, 10))
        
        # 右側のメモ部分
        self.memo_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        self.memo_label.pack(anchor="w", pady=(5, 0))  # 左寄せでラベルを配置
        self.memo.pack(fill=tk.BOTH, expand=True, pady=(2, 5))  # ラベルとの間隔を調整

    def _create_buttons(self):
        """ボタンの作成とレイアウト"""
        for btn in self.BUTTONS:
            command = getattr(self.timer, btn["command"])  # .replace("timer", "")を削除
            button = tk.Button(
                self.timer_frame,
                text=btn["text"],
                command=self._create_command(command, btn),
                width=Styles.SIZES["button_width"],
                relief="flat",
                bg=Styles.COLORS["button_bg"],
                activebackground=Styles.COLORS["button_active"],
                fg=Styles.COLORS["text"],
                font=Styles.FONTS["button"]
            )
            button.grid(
                row=btn["row"],
                column=btn["column"],
                padx=Styles.PADDING["button"],
                pady=Styles.PADDING["button"],
                columnspan=btn.get("columnspan", 1),
                sticky="ew"
            )
            self.buttons[btn["command"]] = button

    def _create_command(self, command, btn):
        """ボタンのコマンド関数を作成"""
        if btn.get("needs_args", True):
            return lambda: command(btn.get("args", 0))
        return command

    def _update_button_states(self):
        """ボタンの状態を更新"""
        if self.timer.running:
            # タイマー実行中の状態
            self.buttons["add_time"]["state"] = "disabled"
            self.buttons["start"]["state"] = "disabled"  # startに変更
            self.buttons["stop"]["state"] = "normal"     # stopに変更
            self.buttons["reset"]["state"] = "disabled"
        else:
            # タイマー停止中の状態
            self.buttons["add_time"]["state"] = "normal"
            self.buttons["start"]["state"] = "normal" if self.timer.time_left > 0 else "disabled"
            self.buttons["stop"]["state"] = "disabled"   # 停止中はストップボタンを無効化
            self.buttons["reset"]["state"] = "normal"

    def update_timer_label(self):
        """タイマーのラベルを更新"""
        hours, remainder = divmod(self.timer.time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self._update_button_states()

    def on_timer_complete(self):
        """タイマー完了時の処理"""
        self._update_button_states()
        messagebox.showinfo("タイマー", f"{self.name}のタイマーが終了しました！")

    def get_memo(self) -> str:
        """メモの内容を取得"""
        return self.memo.get("1.0", tk.END).strip()

    def set_memo(self, text: str) -> None:
        """メモの内容を設定"""
        self.memo.delete("1.0", tk.END)
        self.memo.insert("1.0", text)
        
