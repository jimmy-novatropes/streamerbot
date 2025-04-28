import os
import subprocess
import sys
import shutil  # <-- Add this

PY_FILE_PATH = r"kivy GUI\main.py"  # Adjust as needed
DESTINATION_FOLDER = r"A:\Desktop\Novatropes Stream"  # <-- Change to your desired destination

def build_executable(py_file_path):
    if not os.path.exists(py_file_path):
        print(f"❌ Error: File '{py_file_path}' not found.")
        return

    files_to_include = [
        "server_settings.json",
        "colors.json",
        "rpm.json",
        "saved_settings.json"
    ]

    add_data_args = []
    for file in files_to_include:
        add_data_args += ["--add-data", f"{file};."]

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name", "NovatropeControlApp",
        "--hidden-import", "kivy.core.window.window_sdl2",
        "--hidden-import", "kivy.core.text.text_sdl2",
        *add_data_args,
        py_file_path
    ]

    print(f"▶️ Running: {' '.join(cmd)}")
    subprocess.run(cmd)
    print("\n✅ Build complete! Check the 'dist' folder.")

    # Copy executable
    exe_path = os.path.join("dist", "NovatropeControlApp.exe")
    if os.path.exists(exe_path):
        os.makedirs(DESTINATION_FOLDER, exist_ok=True)
        shutil.copy2(exe_path, DESTINATION_FOLDER)
        print(f"📦 Copied executable to {DESTINATION_FOLDER}")
    else:
        print(f"❌ Could not find {exe_path} to copy.")

if __name__ == "__main__":
    build_executable(PY_FILE_PATH)

