import tkinter as tk
from tkinter import messagebox
from Timer.config.styles import Styles
from Timer.ui.timer_widget import TimerWidget

class TimerApp:
    """複数のタイマーを管理するアプリケーション"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("複数タイマー管理アプリ")
        self.root.configure(bg=Styles.COLORS["bg"])
        
        # ウィンドウサイズの設定
        self.root.minsize(*Styles.SIZES["window_min"])
        self.root.maxsize(*Styles.SIZES["window_max"])
        
        # メインフレームを作成
        self.main_frame = tk.Frame(self.root, bg=Styles.COLORS["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.timers = []
        self._setup_ui()

    def _setup_ui(self):
        """UIの初期設定"""
        self._create_add_timer_frame()
        self._create_scrollable_frame()
        self._setup_scroll_bindings()

    def _create_add_timer_frame(self):
        """タイマー追加用フレームの作成"""
        self.add_timer_frame = tk.Frame(
            self.main_frame,
            bg=Styles.COLORS["frame_bg"],
            relief="ridge",
            borderwidth=1
        )
        self.add_timer_frame.pack(pady=10, fill=tk.X)
        self.add_timer_frame.grid_columnconfigure(1, weight=1)

        tk.Label(
            self.add_timer_frame,
            text="タイマー名:",
            bg=Styles.COLORS["frame_bg"],
            fg=Styles.COLORS["text"],
            font=Styles.FONTS["input"]
        ).grid(row=0, column=0, padx=10, pady=10)
        
        self.timer_name_entry = tk.Entry(
            self.add_timer_frame,
            font=Styles.FONTS["input"]
        )
        self.timer_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        tk.Button(
            self.add_timer_frame,
            text="タイマー追加",
            command=self.add_timer,
            relief="flat",
            bg=Styles.COLORS["accent"],
            fg=Styles.COLORS["accent_text"],
            activebackground=Styles.COLORS["accent_active"],
            font=Styles.FONTS["input"]
        ).grid(row=0, column=2, padx=10, pady=10)

    def _create_scrollable_frame(self):
        """スクロール可能なフレームの作成"""
        self.scroll_frame = tk.Frame(self.main_frame, bg=Styles.COLORS["bg"])
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            self.scroll_frame,
            bg=Styles.COLORS["bg"],
            highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.scroll_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        self.timers_frame = tk.Frame(
            self.canvas,
            bg=Styles.COLORS["bg"]
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.timers_frame,
            anchor="nw",
            width=self.canvas.winfo_width()
        )

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

    def _setup_scroll_bindings(self):
        """スクロールの設定とバインディング"""
        self.timers_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """マウスホイールでのスクロール処理"""
        self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    def _on_frame_configure(self, event=None):
        """フレームのサイズ変更時の処理"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """キャンバスのサイズ変更時の処理"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def add_timer(self):
        """新しいタイマーを追加"""
        name = self.timer_name_entry.get().strip()
        if name:
            timer = TimerWidget(self.timers_frame, name)
            self.timers.append(timer)
            self.timer_name_entry.delete(0, tk.END)
            self._on_frame_configure()
            
            # ウィンドウサイズの自動調整
            current_height = self.root.winfo_height()
            required_height = min(
                Styles.SIZES["window_max"][1],
                self.timers_frame.winfo_reqheight() + 100
            )
            if required_height > current_height:
                self.root.geometry(f"{self.root.winfo_width()}x{required_height}")
        else:
            messagebox.showwarning("警告", "タイマー名を入力してください！")