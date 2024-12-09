#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Time :2024/12/08 17:41:33
@Desc :将视频转换为音频
@Version :1.0
'''
import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES


# --- 工具函数 ---
def select_video():
    filepath = filedialog.askopenfilename(
        filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv")]
    )
    if filepath:
        video_path_var.set(filepath)
        output_name_var.set(os.path.splitext(os.path.basename(filepath))[0])


def select_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_path_var.set(folder)


def start_conversion_thread(params):
    command = params["command"]
    output_path = params["output_path"]
    convert_button.config(state=tk.DISABLED)  # 禁用按钮
    status_var.set("转换中...")
    root.update()
    try:
        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
        status_var.set("转换完成！")
        messagebox.showinfo("成功", f"音频已保存到: {output_path}")
    except FileNotFoundError:  # subprocess.CalledProcessError
        status_var.set("转换失败！")
        messagebox.showerror("错误", "转换失败, 请检查 ffmpeg.exe 是否存在！")
    except Exception as e:
        status_var.set("转换失败！")
        messagebox.showerror("错误", f"转换失败: {str(e)}")
    finally:
        convert_button.config(state=tk.NORMAL)  # 使按钮可用

def on_convert_button_click():
    video_path = video_path_var.get()
    output_folder = output_path_var.get()
    output_filename = output_name_var.get()
    channel = channel_var.get()
    bitrate = bitrate_var.get()
    sample_rate = sample_rate_var.get()
    if not video_path:
        messagebox.showerror("错误", "请先选择视频文件！")
        return
    if not output_folder:
        messagebox.showerror("错误", "请先选择输出路径！")
        return
    if not output_filename:
        messagebox.showerror("错误", "请先设置输出音频名称！")
        return
    if not output_filename.endswith(".mp3"):
        output_filename += ".mp3"
    output_path = os.path.join(output_folder, output_filename)
    channel_flag = "1" if channel == "单声道" else "2"
    # ffmpeg -i input_video.mp4 -vn -ac 2 -b:a 192k -ar 44100 -y output_audio.mp3
    command = [
            "ffmpeg.exe",
            "-i", video_path,
            "-vn",
            "-ac", channel_flag,
            "-b:a", bitrate,
            "-ar", sample_rate,
            "-y",
            output_path
        ]
    params = {
        "command": command,
        "output_path": output_path,
    }
    thread = threading.Thread(target=start_conversion_thread, args=(params,))
    thread.start()


def on_drop(event):
    video_path_var.set(event.data.strip())
    output_name_var.set(os.path.splitext(os.path.basename(event.data.strip()))[0])


def ensure_output_folder():
    default_output_path = os.path.join(os.getcwd(), "output")
    if not os.path.exists(default_output_path):
        os.makedirs(default_output_path)
    output_path_var.set(default_output_path)




# --- 界面 ---
# 创建主窗口
root = TkinterDnD.Tk()
root.title("视频转音频")

# 设置屏幕大小和居中显示
window_width = 630
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 3
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
# 禁止窗口大小调整
root.resizable(False, False)


# 设置图标（.ico 格式）
root.iconbitmap("app.ico")

# 定义变量
video_path_var = tk.StringVar()
output_path_var = tk.StringVar()
output_name_var = tk.StringVar()
channel_var = tk.StringVar(value="双声道")
bitrate_var = tk.StringVar(value="192k")
sample_rate_var = tk.StringVar(value="44100")
status_var = tk.StringVar()
status_var.set("等待中...")

# 确保输出路径存在
ensure_output_folder()

# 样式美化
style = ttk.Style()
root.configure(bg="#F9FAFB")  # 窗口背景色：浅灰白
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), background="#f9fafb", borderwidth=2, bordercolor="#e0e0e0")
style.map("TButton", background=[("active", "#e0eef9")], bordercolor=[("active", "#007ACC")])
style.configure("TLabel", font=("Segoe UI", 11), background="#f9fafb")
style.configure("TEntry", font=("Segoe UI", 11), fieldbackground="#FFFFFF", relief="solid", padding=5, borderwidth=2, bordercolor="#e0e0e0")
style.configure("StatusLabel.TLabel", font=("Segoe UI", 11, "italic"), foreground="#007ACC")
# 设置 Combobox 的样式
style.configure("TCombobox", font=("Segoe UI", 11), padding=2, bordercolor="#e0e0e0", background="#f9f9f9",)
style.map(
    "TCombobox",
    fieldbackground=[("readonly", "#F9FAFB")],  # 只读模式背景颜色
    background=[("active", "#D0E0F0")],        # 活跃项背景颜色
    foreground=[("active", "#000000")],        # 活跃项字体颜色
    bordercolor=[("focus", "#007ACC")],        # 焦点时边框颜色
)
# 美化 Frame 的样式
style.configure(
    "Main.TFrame",
    background="#f9f9f9",  # 背景颜色
    bordercolor="#f9f9f9", # 边框颜色
    borderwidth=1,  # 边框宽度
    relief="solid",  # 边框样式
    padding=10,  # 内部边距
)
style.configure(
    "TFrame",
    background="#f9f9f9",
    bordercolor="#e0e0e0", 
    borderwidth=1,
    relief="solid",
    padding=10,
)

# 主容器
main_frame = ttk.Frame(root, padding="10", style="Main.TFrame")
main_frame.pack(fill="both", expand=False, padx=10, pady=10)

# 视频路径
ttk.Label(main_frame, text="视频文件:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
video_entry = ttk.Entry(main_frame, textvariable=video_path_var, width=45)
video_entry.grid(row=0, column=1, padx=10, pady=10)
ttk.Button(main_frame, text="选择文件", command=select_video, padding=(5, 3)).grid(row=0, column=2, padx=10, pady=10)

# 输出路径
ttk.Label(main_frame, text="输出路径:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_entry = ttk.Entry(main_frame, textvariable=output_path_var, width=45)
output_entry.grid(row=1, column=1, padx=10, pady=10)
ttk.Button(main_frame, text="选择路径", command=select_output_folder, padding=(5, 3)).grid(row=1, column=2, padx=10, pady=10)

# 输出文件名
ttk.Label(main_frame, text="输出名称:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
output_name_entry = ttk.Entry(main_frame, textvariable=output_name_var, width=45)
output_name_entry.grid(row=2, column=1, padx=10, pady=10)
ttk.Label(main_frame, text=".mp3", padding=(5, 3)).grid(row=2, column=2, padx=10, pady=10, sticky="w")


# 转换参数框架
parameter_frame = ttk.Frame(main_frame, padding="5", style="TFrame")
parameter_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

# 转换参数标题
ttk.Label(parameter_frame, text="   转换参数", font=("Segoe UI", 11)).grid(row=0, column=0, columnspan=6, pady=(0, 10), sticky="w")

# 参数水平排列
ttk.Label(parameter_frame, text="声道:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
channel_combo = ttk.Combobox(parameter_frame, textvariable=channel_var, values=["单声道", "双声道"], state="readonly", width=12)
channel_combo.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(parameter_frame, text="比特率:").grid(row=1, column=2, padx=10, pady=10, sticky="e")
bitrate_combo = ttk.Combobox(parameter_frame, textvariable=bitrate_var, values=["128k", "192k", "320k"], state="readonly", width=12)
bitrate_combo.grid(row=1, column=3, padx=10, pady=10)

ttk.Label(parameter_frame, text="采样率:").grid(row=1, column=4, padx=10, pady=10, sticky="e")
sample_rate_combo = ttk.Combobox(parameter_frame, textvariable=sample_rate_var, values=["44100", "48000"], state="readonly", width=12)
sample_rate_combo.grid(row=1, column=5, padx=10, pady=10)

# 转换按钮 (调整位置到 parameter_frame 下方)
convert_button = ttk.Button(main_frame, text="开始转换", command=on_convert_button_click, width=20)
convert_button.grid(row=4, column=0, columnspan=3, pady=10, sticky="n")

# 转换状态
status_label = ttk.Label(root, textvariable=status_var, style="StatusLabel.TLabel", anchor="center", background="#F9FAFB")
status_label.pack(pady=6)

# 拖拽功能
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)

# 启动主循环
root.mainloop()
