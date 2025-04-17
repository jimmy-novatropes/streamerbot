# import os
# import subprocess
# import sys
#
# # 🔧 SET YOUR PYTHON FILE PATH HERE
# PY_FILE_PATH = r"C:\Users\BloomTech\Documents\twitch streaming\streamerbot\new approach to data sharing\GUI Build\main.py"  # Replace with your actual script path
#
#
# def build_executable(py_file_path):
#     if not os.path.exists(py_file_path):
#         print(f"❌ Error: File '{py_file_path}' not found.")
#         return
#
#     # Call pyinstaller using the current Python environment
#     # cmd = [
#     #     sys.executable, "-m", "PyInstaller",
#     #     "--onefile",
#     #     "--clean",
#     #     py_file_path
#     # ]
#     cmd = [
#         sys.executable, "-m", "PyInstaller",
#         "--onefile",
#         "--add-data", "server_settings.json;.",  # Windows uses ";" separator
#         py_file_path
#     ]
#
#     print(f"▶️ Running: {' '.join(cmd)}")
#     subprocess.run(cmd)
#     print("\n✅ Build complete! Check the 'dist' folder.")
#
# if __name__ == "__main__":
#     build_executable(PY_FILE_PATH)
#
import os
import subprocess
import sys

PY_FILE_PATH = r"GUI Build\main.py"  # adjust as needed


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

    # Build --add-data args
    add_data_args = []
    for file in files_to_include:
        add_data_args += ["--add-data", f"{file};."]

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        # "--windowed",
        "--clean",
        # "--debug=all",
        # *add_data_args,
        py_file_path
    ]

    print(f"▶️ Running: {' '.join(cmd)}")
    subprocess.run(cmd)
    print("\n✅ Build complete! Check the 'dist' folder.")


if __name__ == "__main__":
    build_executable(PY_FILE_PATH)
