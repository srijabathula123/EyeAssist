import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import json
from pathlib import Path


class EyeAssistDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("EyeAssist - AI-Based Eye Control System")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#0f172a")

        self.base_dir = Path(__file__).resolve().parent

        self.eye_process = None
        self.voice_process = None

        self.colors = {
            "bg": "#0f172a",
            "sidebar": "#111827",
            "card": "#1e293b",
            "text": "#f8fafc",
            "muted": "#94a3b8",
            "accent": "#38bdf8",
            "green": "#22c55e",
            "red": "#ef4444",
            "yellow": "#f59e0b",
            "border": "#334155"
        }

        self.current_section = "Dashboard"

        self.build_sidebar()
        self.build_main()

        self.show_dashboard()
        self.update_status_loop()

        self.root.protocol("WM_DELETE_WINDOW", self.close_dashboard)

    # =========================
    # SIDEBAR
    # =========================

    def build_sidebar(self):
        self.sidebar = tk.Frame(
            self.root,
            bg=self.colors["sidebar"],
            width=240
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="◉ EyeAssist",
            font=("Segoe UI", 22, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["sidebar"]
        ).pack(pady=(35, 8))

        tk.Label(
            self.sidebar,
            text="AI Accessibility System",
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg=self.colors["sidebar"]
        ).pack(pady=(0, 35))

        self.nav_buttons = {}

        self.create_nav_button("🏠", "Dashboard", self.show_dashboard)
        self.create_nav_button("👁", "Eye Control", self.show_eye_control)
        self.create_nav_button("🎙", "Voice Control", self.show_voice_control)
        self.create_nav_button("🤖", "AI Model", self.show_ai_model)
        self.create_nav_button("⚙", "System", self.show_system)

        bottom = tk.Frame(
            self.sidebar,
            bg=self.colors["sidebar"]
        )
        bottom.pack(side="bottom", fill="x", pady=25)

        tk.Label(
            bottom,
            text="EyeAssist v1.0",
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg=self.colors["sidebar"]
        ).pack()

        tk.Label(
            bottom,
            text="Accessibility • AI • Vision",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg=self.colors["sidebar"]
        ).pack(pady=5)

    def create_nav_button(self, icon, name, command):
        button = tk.Button(
            self.sidebar,
            text=f"{icon}   {name}",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            padx=18,
            pady=12,
            bd=0,
            relief="flat",
            fg=self.colors["muted"],
            bg=self.colors["sidebar"],
            activeforeground=self.colors["text"],
            activebackground="#1e293b",
            cursor="hand2",
            command=command
        )

        button.pack(fill="x", padx=15, pady=4)

        self.nav_buttons[name] = button

    def set_active_nav(self, name):
        for item, button in self.nav_buttons.items():
            if item == name:
                button.configure(
                    bg="#1e293b",
                    fg=self.colors["accent"]
                )
            else:
                button.configure(
                    bg=self.colors["sidebar"],
                    fg=self.colors["muted"]
                )

    # =========================
    # MAIN
    # =========================

    def build_main(self):
        self.main = tk.Frame(
            self.root,
            bg=self.colors["bg"]
        )
        self.main.pack(side="left", fill="both", expand=True)

        self.topbar = tk.Frame(
            self.main,
            bg=self.colors["bg"]
        )
        self.topbar.pack(
            fill="x",
            padx=35,
            pady=(25, 0)
        )

        self.page_title = tk.Label(
            self.topbar,
            text="Dashboard",
            font=("Segoe UI", 25, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        )
        self.page_title.pack(side="left")

        self.system_status = tk.Label(
            self.topbar,
            text="● SYSTEM READY",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["green"],
            bg=self.colors["bg"]
        )
        self.system_status.pack(side="right")

        self.content = tk.Frame(
            self.main,
            bg=self.colors["bg"]
        )
        self.content.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # =========================
    # CARDS
    # =========================

    def create_card(
        self,
        parent,
        title,
        value,
        subtitle,
        color
    ):
        card = tk.Frame(
            parent,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["card"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 18, "bold"),
            fg=color,
            bg=self.colors["card"]
        )
        value_label.pack(anchor="w", padx=20)

        subtitle_label = tk.Label(
            card,
            text=subtitle,
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg=self.colors["card"]
        )
        subtitle_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 18)
        )

        card.value_label = value_label
        card.subtitle_label = subtitle_label

        return card

    def update_card(
        self,
        card,
        value,
        subtitle,
        color
    ):
        if card and card.winfo_exists():
            card.value_label.configure(
                text=value,
                fg=color
            )
            card.subtitle_label.configure(
                text=subtitle
            )

    # =========================
    # DASHBOARD
    # =========================

    def show_dashboard(self):
        self.current_section = "Dashboard"
        self.set_active_nav("Dashboard")
        self.page_title.configure(text="Dashboard")
        self.clear_content()

        tk.Label(
            self.content,
            text="EyeAssist Control Center",
            font=("Segoe UI", 15, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(anchor="w", pady=(0, 15))

        cards = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        cards.pack(fill="x")

        self.dashboard_camera = self.create_card(
            cards,
            "CAMERA",
            "READY",
            "Webcam input",
            self.colors["green"]
        )
        self.dashboard_camera.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        self.dashboard_eye = self.create_card(
            cards,
            "EYE CONTROL",
            "STOPPED",
            "AI mouse control",
            self.colors["red"]
        )
        self.dashboard_eye.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )

        self.dashboard_voice = self.create_card(
            cards,
            "VOICE CONTROL",
            "STOPPED",
            "Voice assistant",
            self.colors["red"]
        )
        self.dashboard_voice.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )

        self.dashboard_model = self.create_card(
            cards,
            "AI MODEL",
            "RANDOM FOREST",
            "Gesture classification",
            self.colors["accent"]
        )
        self.dashboard_model.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        activity = tk.Frame(
            self.content,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        activity.pack(
            fill="both",
            expand=True,
            pady=(20, 15)
        )

        tk.Label(
            activity,
            text="System Activity",
            font=("Segoe UI", 13, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.activity_text = tk.Text(
            activity,
            height=10,
            bg="#111827",
            fg="#cbd5e1",
            insertbackground="white",
            bd=0,
            font=("Consolas", 10),
            state="disabled"
        )
        self.activity_text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        controls = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        controls.pack(fill="x")

        tk.Button(
            controls,
            text="▶  Start Eye Control",
            command=self.start_eye_control,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#0284c7",
            activebackground="#0369a1",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            controls,
            text="🎙  Start Voice Control",
            command=self.start_voice_control,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#0284c7",
            activebackground="#0369a1",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=10)

        tk.Button(
            controls,
            text="■  Stop Eye Control",
            command=self.stop_eye_control,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#dc2626",
            activebackground="#b91c1c",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="right")

        self.log_activity("Dashboard opened.")

    # =========================
    # EYE CONTROL
    # =========================

    def show_eye_control(self):
        self.current_section = "Eye Control"
        self.set_active_nav("Eye Control")
        self.page_title.configure(text="Eye Control")
        self.clear_content()

        tk.Label(
            self.content,
            text="AI Eye-Controlled Mouse",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(anchor="w", pady=(5, 20))

        cards = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        cards.pack(fill="x")

        self.eye_status_card = self.create_card(
            cards,
            "STATUS",
            "STOPPED",
            "ai_mouse_control.py",
            self.colors["red"]
        )
        self.eye_status_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.calibration_card = self.create_card(
            cards,
            "CALIBRATION",
            "AUTOMATIC",
            "Re-calibrates for a new face",
            self.colors["accent"]
        )
        self.calibration_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.gesture_card = self.create_card(
            cards,
            "GESTURES",
            "ENABLED",
            "Eye movement + blink gestures",
            self.colors["green"]
        )
        self.gesture_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        info = tk.Frame(
            self.content,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        info.pack(fill="both", expand=True, pady=25)

        tk.Label(
            info,
            text="Supported Eye Gestures",
            font=("Segoe UI", 13, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 12)
        )

        gestures = [
            ("Look Left / Right / Up / Down", "Move cursor"),
            ("Left Eye Blink", "Left click"),
            ("Right Eye Blink", "Right click"),
            ("Both Eyes Blink", "Double left click"),
            ("P", "Pause / Resume"),
            ("Q", "Exit eye control")
        ]

        for gesture, action in gestures:
            row = tk.Frame(
                info,
                bg=self.colors["card"]
            )
            row.pack(
                fill="x",
                padx=20,
                pady=4
            )

            tk.Label(
                row,
                text=gesture,
                width=30,
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                fg=self.colors["text"],
                bg=self.colors["card"]
            ).pack(side="left")

            tk.Label(
                row,
                text=action,
                anchor="w",
                font=("Segoe UI", 10),
                fg=self.colors["muted"],
                bg=self.colors["card"]
            ).pack(side="left")

        controls = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        controls.pack(fill="x")

        tk.Button(
            controls,
            text="▶  Start Eye Control",
            command=self.start_eye_control,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#0284c7",
            activebackground="#0369a1",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            controls,
            text="■  Stop",
            command=self.stop_eye_control,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#dc2626",
            activebackground="#b91c1c",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=10)

    # =========================
    # VOICE CONTROL
    # =========================

    def show_voice_control(self):
        self.current_section = "Voice Control"
        self.set_active_nav("Voice Control")
        self.page_title.configure(text="Voice Control")
        self.clear_content()

        tk.Label(
            self.content,
            text="Voice Accessibility Assistant",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(anchor="w", pady=(5, 20))

        cards = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        cards.pack(fill="x")

        self.voice_status_card = self.create_card(
            cards,
            "VOICE STATUS",
            "STOPPED",
            "Waiting to start",
            self.colors["red"]
        )
        self.voice_status_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.last_spoken_card = self.create_card(
            cards,
            "LAST SPOKEN",
            "—",
            "No command yet",
            self.colors["accent"]
        )
        self.last_spoken_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.voice_command_card = self.create_card(
            cards,
            "LAST COMMAND",
            "—",
            "No command yet",
            self.colors["green"]
        )
        self.voice_command_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        activity = tk.Frame(
            self.content,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        activity.pack(
            fill="both",
            expand=True,
            pady=25
        )

        tk.Label(
            activity,
            text="Voice Activity",
            font=("Segoe UI", 13, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.voice_message = tk.Label(
            activity,
            text="Voice control is currently stopped.",
            font=("Segoe UI", 12),
            fg=self.colors["muted"],
            bg=self.colors["card"],
            wraplength=700,
            justify="left"
        )
        self.voice_message.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        controls = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        controls.pack(fill="x")

        tk.Button(
            controls,
            text="🎙  Start Voice Control",
            command=self.start_voice_control,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#0284c7",
            activebackground="#0369a1",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            controls,
            text="■  Stop Voice Control",
            command=self.stop_voice_control,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#dc2626",
            activebackground="#b91c1c",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=10)

    # =========================
    # AI MODEL
    # =========================

    def show_ai_model(self):
        self.current_section = "AI Model"
        self.set_active_nav("AI Model")
        self.page_title.configure(text="AI Model")
        self.clear_content()

        tk.Label(
            self.content,
            text="Eye Gesture Intelligence",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(anchor="w", pady=(5, 20))

        cards = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        cards.pack(fill="x")

        self.create_card(
            cards,
            "MODEL",
            "RANDOM FOREST",
            "Machine learning classifier",
            self.colors["accent"]
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.create_card(
            cards,
            "FEATURES",
            "10",
            "Eye and gaze features",
            self.colors["green"]
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.create_card(
            cards,
            "TEST ACCURACY",
            "92.47%",
            "Current prototype evaluation",
            self.colors["yellow"]
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        info = tk.Frame(
            self.content,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        info.pack(
            fill="both",
            expand=True,
            pady=25
        )

        tk.Label(
            info,
            text="Model Information",
            font=("Segoe UI", 14, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        information = [
            ("Algorithm", "Random Forest Classifier"),
            ("Input", "Eye and iris features"),
            ("Classes", "8 eye gestures"),
            ("Model File", "eye_gesture_model.pkl"),
            ("Training Samples", "2125"),
            ("Purpose", "Recognize eye gestures for computer control")
        ]

        for key, value in information:
            row = tk.Frame(
                info,
                bg=self.colors["card"]
            )
            row.pack(
                fill="x",
                padx=20,
                pady=6
            )

            tk.Label(
                row,
                text=key,
                width=22,
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                fg=self.colors["muted"],
                bg=self.colors["card"]
            ).pack(side="left")

            tk.Label(
                row,
                text=value,
                anchor="w",
                font=("Segoe UI", 10),
                fg=self.colors["text"],
                bg=self.colors["card"]
            ).pack(side="left")

    # =========================
    # SYSTEM
    # =========================

    def show_system(self):
        self.current_section = "System"
        self.set_active_nav("System")
        self.page_title.configure(text="System")
        self.clear_content()

        tk.Label(
            self.content,
            text="System Information",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg"]
        ).pack(anchor="w", pady=(5, 20))

        cards = tk.Frame(
            self.content,
            bg=self.colors["bg"]
        )
        cards.pack(fill="x")

        self.system_eye = self.create_card(
            cards,
            "EYE PROCESS",
            "STOPPED",
            "ai_mouse_control.py",
            self.colors["red"]
        )
        self.system_eye.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.system_voice = self.create_card(
            cards,
            "VOICE PROCESS",
            "STOPPED",
            "voice_control.py",
            self.colors["red"]
        )
        self.system_voice.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.create_card(
            cards,
            "CAMERA",
            "READY",
            "OpenCV camera input",
            self.colors["green"]
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        self.create_card(
            cards,
            "MODEL",
            "LOADED",
            "eye_gesture_model.pkl",
            self.colors["green"]
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        info = tk.Frame(
            self.content,
            bg=self.colors["card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        info.pack(
            fill="both",
            expand=True,
            pady=25
        )

        tk.Label(
            info,
            text="Project Components",
            font=("Segoe UI", 14, "bold"),
            fg=self.colors["text"],
            bg=self.colors["card"]
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        components = [
            "Python",
            "OpenCV",
            "MediaPipe",
            "NumPy",
            "Random Forest",
            "scikit-learn",
            "PyAutoGUI",
            "SpeechRecognition",
            "PyAudio"
        ]

        for component in components:
            tk.Label(
                info,
                text=f"●  {component}",
                font=("Segoe UI", 10),
                fg=self.colors["muted"],
                bg=self.colors["card"]
            ).pack(
                anchor="w",
                padx=25,
                pady=3
            )

    # =========================
    # PROCESS FUNCTIONS
    # =========================

    def start_eye_control(self):
        if self.is_running(self.eye_process):
            self.log_activity("Eye Control is already running.")
            return

        path = self.base_dir / "ai_mouse_control.py"

        if not path.exists():
            messagebox.showerror(
                "File Not Found",
                f"Could not find:\n{path}"
            )
            return

        try:
            self.eye_process = subprocess.Popen(
                [sys.executable, str(path)],
                cwd=str(self.base_dir)
            )

            self.log_activity(
                "Eye Control started."
            )

            self.refresh_current_page()

        except Exception as e:
            messagebox.showerror(
                "Eye Control Error",
                str(e)
            )

    def stop_eye_control(self):
        if not self.is_running(self.eye_process):
            self.log_activity(
                "Eye Control is not running."
            )
            self.eye_process = None
            self.refresh_current_page()
            return

        try:
            self.eye_process.terminate()
            self.eye_process.wait(timeout=2)

        except subprocess.TimeoutExpired:
            self.eye_process.kill()

        except Exception as e:
            self.log_activity(
                f"Eye Control stop error: {e}"
            )

        self.eye_process = None

        self.log_activity(
            "Eye Control stopped."
        )

        self.refresh_current_page()

    def start_voice_control(self):
        if self.is_running(self.voice_process):
            self.log_activity(
                "Voice Control is already running."
            )
            return

        path = self.base_dir / "voice_control.py"

        if not path.exists():
            messagebox.showerror(
                "File Not Found",
                f"Could not find:\n{path}"
            )
            return

        try:
            self.voice_process = subprocess.Popen(
                [sys.executable, str(path)],
                cwd=str(self.base_dir)
            )

            self.log_activity(
                "Voice Control started."
            )

            self.refresh_current_page()

        except Exception as e:
            messagebox.showerror(
                "Voice Control Error",
                str(e)
            )

    def stop_voice_control(self):
        if not self.is_running(self.voice_process):
            self.log_activity(
                "Voice Control is not running."
            )
            self.voice_process = None
            self.refresh_current_page()
            return

        try:
            self.voice_process.terminate()
            self.voice_process.wait(timeout=2)

        except subprocess.TimeoutExpired:
            self.voice_process.kill()

        except Exception as e:
            self.log_activity(
                f"Voice Control stop error: {e}"
            )

        self.voice_process = None

        self.log_activity(
            "Voice Control stopped."
        )

        self.refresh_current_page()

    def is_running(self, process):
        return (
            process is not None
            and process.poll() is None
        )

    # =========================
    # VOICE STATUS
    # =========================

    def read_voice_status(self):
        path = self.base_dir / "voice_status.json"

        if not path.exists():
            return None

        try:
            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except Exception:
            return None

    # =========================
    # REFRESH
    # =========================

    def refresh_current_page(self):
        if self.current_section == "Eye Control":
            self.show_eye_control()

        elif self.current_section == "Voice Control":
            self.show_voice_control()

        elif self.current_section == "System":
            self.show_system()

        elif self.current_section == "Dashboard":
            self.show_dashboard()

    def update_status_loop(self):
        eye_running = self.is_running(
            self.eye_process
        )

        voice_running = self.is_running(
            self.voice_process
        )

        if eye_running or voice_running:
            self.system_status.configure(
                text="● SYSTEM ACTIVE",
                fg=self.colors["green"]
            )
        else:
            self.system_status.configure(
                text="● SYSTEM READY",
                fg=self.colors["green"]
            )

        if self.current_section == "Dashboard":
            if hasattr(self, "dashboard_eye"):
                self.update_card(
                    self.dashboard_eye,
                    "RUNNING" if eye_running else "STOPPED",
                    "AI mouse control",
                    self.colors["green"]
                    if eye_running
                    else self.colors["red"]
                )

            if hasattr(self, "dashboard_voice"):
                data = self.read_voice_status()

                if voice_running:
                    status = (
                        data.get("status", "LISTENING")
                        if data
                        else "LISTENING"
                    )

                    self.update_card(
                        self.dashboard_voice,
                        status,
                        "Voice assistant",
                        self.colors["green"]
                    )
                else:
                    self.update_card(
                        self.dashboard_voice,
                        "STOPPED",
                        "Voice assistant",
                        self.colors["red"]
                    )

        if self.current_section == "Voice Control":
            self.update_voice_page()

        if self.current_section == "System":
            if hasattr(self, "system_eye"):
                self.update_card(
                    self.system_eye,
                    "RUNNING" if eye_running else "STOPPED",
                    "ai_mouse_control.py",
                    self.colors["green"]
                    if eye_running
                    else self.colors["red"]
                )

            if hasattr(self, "system_voice"):
                self.update_card(
                    self.system_voice,
                    "RUNNING" if voice_running else "STOPPED",
                    "voice_control.py",
                    self.colors["green"]
                    if voice_running
                    else self.colors["red"]
                )

        self.root.after(
            1000,
            self.update_status_loop
        )

    def update_voice_page(self):
        data = self.read_voice_status()

        if not data:
            return

        status = data.get(
            "status",
            "STOPPED"
        )

        spoken = data.get(
            "last_spoken",
            ""
        )

        command = data.get(
            "command",
            ""
        )

        message = data.get(
            "message",
            ""
        )

        if not self.is_running(self.voice_process):
            status = "STOPPED"
            color = self.colors["red"]
        elif status == "ERROR":
            color = self.colors["red"]
        else:
            color = self.colors["green"]

        if hasattr(self, "voice_status_card"):
            self.update_card(
                self.voice_status_card,
                status,
                "Live voice status",
                color
            )

        if hasattr(self, "last_spoken_card"):
            self.update_card(
                self.last_spoken_card,
                spoken if spoken else "—",
                "Most recent recognized speech",
                self.colors["accent"]
            )

        if hasattr(self, "voice_command_card"):
            self.update_card(
                self.voice_command_card,
                command if command else "—",
                "Command processed",
                self.colors["green"]
            )

        if hasattr(self, "voice_message"):
            self.voice_message.configure(
                text=message
                if message
                else "Waiting for voice command."
            )

    # =========================
    # LOG
    # =========================

    def log_activity(self, message):
        if not hasattr(self, "activity_text"):
            return

        try:
            self.activity_text.configure(
                state="normal"
            )

            self.activity_text.insert(
                "end",
                f"• {message}\n"
            )

            self.activity_text.see("end")

            self.activity_text.configure(
                state="disabled"
            )

        except tk.TclError:
            pass

    # =========================
    # CLOSE
    # =========================

    def close_dashboard(self):
        try:
            if self.is_running(
                self.eye_process
            ):
                self.eye_process.terminate()

            if self.is_running(
                self.voice_process
            ):
                self.voice_process.terminate()

        except Exception:
            pass

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EyeAssistDashboard(root)
    root.mainloop()