import speech_recognition as sr
import pyautogui
import webbrowser
import urllib.parse
import subprocess
import os
import time
from pathlib import Path


recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.5
recognizer.phrase_threshold = 0.2

last_typed_text = ""


def open_windows_app(name):

    try:
        pyautogui.press("win")
        time.sleep(0.5)

        pyautogui.write(name, interval=0.03)
        time.sleep(1)

        pyautogui.press("enter")
        time.sleep(2)

        print("Opened:", name)

        return True

    except Exception as error:
        print("Could not open application:", error)
        return False


def open_special_folder(name):

    name = name.lower().strip()
    home = Path.home()

    folders = {
        "desktop": [
            home / "Desktop",
            home / "OneDrive" / "Desktop"
        ],

        "my desktop": [
            home / "Desktop",
            home / "OneDrive" / "Desktop"
        ],

        "documents": [
            home / "Documents",
            home / "OneDrive" / "Documents"
        ],

        "my documents": [
            home / "Documents",
            home / "OneDrive" / "Documents"
        ],

        "downloads": [
            home / "Downloads",
            home / "OneDrive" / "Downloads"
        ],

        "my downloads": [
            home / "Downloads",
            home / "OneDrive" / "Downloads"
        ],

        "pictures": [
            home / "Pictures",
            home / "OneDrive" / "Pictures"
        ],

        "videos": [
            home / "Videos",
            home / "OneDrive" / "Videos"
        ],

        "music": [
            home / "Music",
            home / "OneDrive" / "Music"
        ]
    }

    if name in [
        "files",
        "my files",
        "file explorer",
        "explorer",
        "computer",
        "my computer"
    ]:

        subprocess.Popen("explorer.exe")
        time.sleep(1)

        return True

    if name in folders:

        for folder in folders[name]:

            if folder.exists():

                subprocess.Popen([
                    "explorer.exe",
                    str(folder)
                ])

                time.sleep(1)

                return True

    return False


def search_file(name):

    home = Path.home()

    locations = [
        home / "Desktop",
        home / "Documents",
        home / "Downloads",
        home / "Pictures",
        home / "Videos",
        home / "Music",
        home / "OneDrive" / "Desktop",
        home / "OneDrive" / "Documents",
        home / "OneDrive" / "Downloads",
        home / "OneDrive" / "Pictures"
    ]

    for folder in locations:

        if not folder.exists():
            continue

        try:

            for item in folder.rglob("*"):

                try:

                    if item.is_file():

                        if item.name.lower() == name.lower():
                            return item

                        if item.stem.lower() == name.lower():
                            return item

                except:
                    continue

        except:
            continue

    return None


def open_file(path):

    try:

        os.startfile(str(path))

        time.sleep(2)

        print("Opened:", path)

        return True

    except Exception as error:

        print("File error:", error)

        return False


def open_anything(name):

    name = name.lower().strip()

    if open_special_folder(name):
        return

    websites = {

        "youtube":
            "https://www.youtube.com",

        "google":
            "https://www.google.com",

        "chatgpt":
            "https://chatgpt.com",

        "gmail":
            "https://mail.google.com",

        "github":
            "https://github.com",

        "instagram":
            "https://www.instagram.com",

        "facebook":
            "https://www.facebook.com"
    }

    if name in websites:

        webbrowser.open(websites[name])

        time.sleep(2)

        return

    applications = {

        "chrome": "chrome",

        "google chrome": "chrome",

        "notepad": "notepad",

        "calculator": "calculator",

        "paint": "paint",

        "vs code": "visual studio code",

        "vscode": "visual studio code",

        "visual studio code": "visual studio code",

        "whatsapp": "whatsapp",

        "edge": "microsoft edge",

        "microsoft edge": "microsoft edge",

        "word": "word",

        "excel": "excel",

        "powerpoint": "powerpoint",

        "settings": "settings"
    }

    if name in applications:

        open_windows_app(
            applications[name]
        )

        return

    extensions = [
        ".pdf",
        ".docx",
        ".doc",
        ".txt",
        ".jpg",
        ".jpeg",
        ".png",
        ".xlsx",
        ".xls",
        ".ppt",
        ".pptx",
        ".csv",
        ".py",
        ".java",
        ".cpp",
        ".html",
        ".css",
        ".js",
        ".mp4",
        ".mp3"
    ]

    if any(name.endswith(ext) for ext in extensions):

        file_path = search_file(name)

        if file_path:
            open_file(file_path)
        else:
            print("File not found:", name)

        return

    open_windows_app(name)


def search_web(text):

    if not text:

        print("Nothing to search.")

        return

    url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote(text)
    )

    webbrowser.open(url)

    print("Searching:", text)


def handle_command(command):

    global last_typed_text

    command = command.lower().strip()

    print()
    print("You said:", command)

    # STOP

    stop_commands = [
        "stop",
        "exit",
        "quit",
        "stop voice control",
        "stop listening",
        "close voice control",
        "turn off voice control"
    ]

    if command in stop_commands:

        print("Stopping voice control...")

        return False

    if (
        command.startswith("stop voice")
        or command.startswith("exit voice")
        or command.startswith("quit voice")
    ):

        print("Stopping voice control...")

        return False

    # CLOSE

    if command in [
        "close window",
        "close current window",
        "close this window",
        "close"
    ]:

        pyautogui.hotkey(
            "alt",
            "f4"
        )

        print("Closed current window")

        return True

    # MINIMIZE

    if command in [
        "minimize window",
        "minimise window",
        "minimize",
        "minimise"
    ]:

        pyautogui.hotkey(
            "win",
            "down"
        )

        print("Minimized current window")

        return True

    # MAXIMIZE

    if command in [
        "maximize window",
        "maximise window",
        "maximize",
        "maximise"
    ]:

        pyautogui.hotkey(
            "win",
            "up"
        )

        print("Maximized current window")

        return True

    # MOUSE

    if "double click" in command:

        pyautogui.doubleClick()

        print("Double click")

        return True

    if "right click" in command:

        pyautogui.rightClick()

        print("Right click")

        return True

    if (
        command == "click"
        or "left click" in command
    ):

        pyautogui.click()

        print("Left click")

        return True

    # SCROLL

    if "scroll down" in command:

        pyautogui.press("pagedown")

        print("Scrolled down")

        return True

    if "scroll up" in command:

        pyautogui.press("pageup")

        print("Scrolled up")

        return True

    # COPY

    if command == "copy" or "copy this" in command:

        pyautogui.hotkey(
            "ctrl",
            "c"
        )

        print("Copied")

        return True

    # PASTE

    if command == "paste" or "paste this" in command:

        pyautogui.hotkey(
            "ctrl",
            "v"
        )

        print("Pasted")

        return True

    # CUT

    if command == "cut":

        pyautogui.hotkey(
            "ctrl",
            "x"
        )

        print("Cut")

        return True

    # SELECT ALL

    if "select all" in command:

        pyautogui.hotkey(
            "ctrl",
            "a"
        )

        print("Selected all")

        return True

    # UNDO

    if command == "undo":

        pyautogui.hotkey(
            "ctrl",
            "z"
        )

        print("Undo")

        return True

    # REDO

    if command == "redo":

        pyautogui.hotkey(
            "ctrl",
            "y"
        )

        print("Redo")

        return True

    # TYPE

    if command.startswith("type "):

        text = command[5:].strip()

        if text:

            pyautogui.write(
                text,
                interval=0.03
            )

            last_typed_text = text

            print(
                "Typed:",
                text
            )

        return True

    # SEARCH PREVIOUSLY TYPED TEXT

    if command == "search":

        if last_typed_text:

            pyautogui.hotkey(
                "ctrl",
                "l"
            )

            time.sleep(0.2)

            pyautogui.write(
                last_typed_text,
                interval=0.03
            )

            pyautogui.press("enter")

            print(
                "Searching:",
                last_typed_text
            )

        else:

            print(
                "No previous text to search."
            )

        return True

    # SEARCH DIRECTLY

    if command.startswith("search for "):

        text = command[11:].strip()

        search_web(text)

        return True

    if command.startswith("search "):

        text = command[7:].strip()

        if text:
            search_web(text)

        return True

    # PRESS KEY

    keys = {

        "enter": "enter",
        "escape": "esc",
        "esc": "esc",
        "space": "space",
        "tab": "tab",
        "backspace": "backspace",
        "delete": "delete",
        "home": "home",
        "end": "end",
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right",
        "page up": "pageup",
        "page down": "pagedown"
    }

    if command.startswith("press "):

        key_name = command[6:].strip()

        if key_name in keys:

            pyautogui.press(
                keys[key_name]
            )

            print(
                "Pressed:",
                key_name
            )

        return True

    # BACK

    if command in [
        "back",
        "go back"
    ]:

        pyautogui.hotkey(
            "alt",
            "left"
        )

        print("Back")

        return True

    # FORWARD

    if command in [
        "forward",
        "go forward"
    ]:

        pyautogui.hotkey(
            "alt",
            "right"
        )

        print("Forward")

        return True

    # OPEN

    if command.startswith("open "):

        item = command[5:].strip()

        open_anything(item)

        return True

    # SHOW DESKTOP

    if command == "show desktop":

        pyautogui.hotkey(
            "win",
            "d"
        )

        print("Desktop shown")

        return True

    # LOCK

    if (
        command == "lock computer"
        or command == "lock screen"
    ):

        pyautogui.hotkey(
            "win",
            "l"
        )

        print("Computer locked")

        return True

    print(
        "Command not recognized."
    )

    return True


print()
print("========================================")
print("        EYEASSIST VOICE CONTROL")
print("========================================")
print()
print("Universal computer voice control")
print()
print("Starting microphone...")
print()


with sr.Microphone() as source:

    recognizer.adjust_for_ambient_noise(
        source,
        duration=0.5
    )

    print()
    print("VOICE CONTROL READY!")
    print()

    while True:

        try:

            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=3,
                phrase_time_limit=5
            )

            print("Processing...")

            command = recognizer.recognize_google(
                audio
            )

            if not handle_command(command):

                break

        except sr.WaitTimeoutError:

            print(
                "No speech detected."
            )

        except sr.UnknownValueError:

            print(
                "Could not understand."
            )

        except sr.RequestError:

            print(
                "Speech recognition service error."
            )

        except KeyboardInterrupt:

            print()
            print(
                "Voice control stopped."
            )

            break


print()
print("========================================")
print("     EYEASSIST VOICE CONTROL STOPPED")
print("========================================")