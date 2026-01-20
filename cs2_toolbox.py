import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import time
import ctypes
import os
import sys
import pyperclip
import threading
import random
import webbrowser  # 用于打开博客链接
from PIL import Image, ImageTk

# ===================== 必看：解决权限问题 =====================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    messagebox.showerror("权限不足", "必须右键→以管理员身份运行！")
    sys.exit(1)

# ===================== 全局变量 =====================
MSG_FILE = "cs2_msg.txt"
FIRE_FILE = "cs2_fire_config.txt"
MSG_LIST = ["牛魔的", "菜就多练", "拿下", "ez", "别送了兄弟"]
# 更新开火默认词汇（贴合CS2场景）
FIRE_CONFIG = {"mode": 0, "texts": ["冲就完事了！", "这波我来Carry", "别白给！跟我上"], "index": 0}

# ===================== 主窗口初始化（保留好看的UI） =====================
root = tk.Tk()
root.title("CS2工具箱")  # 改名为CS2工具箱
root.geometry("500x650+100+100")
root.attributes('-topmost', True)
root.config(bg="#222222")  # 基础深色背景，保留好看的UI

# ===================== 核心功能（保留所有原有逻辑） =====================
def send_zh(msg):
    try:
        pyperclip.copy(msg)
        time.sleep(0.05)
        
        def press_key(vk, hold=0.03):
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
            time.sleep(hold)
            ctypes.windll.user32.keybd_event(vk, 0, 2, 0)
            time.sleep(0.01)
        
        press_key(0x59)
        time.sleep(0.1)
        ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)
        time.sleep(0.02)
        press_key(0x56, 0.02)
        ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)
        time.sleep(0.05)
        press_key(0x0D)
        print(f"✅ 发送成功：{msg}")
    except Exception as e:
        messagebox.showwarning("发送失败", f"CS2需在前台！\n错误：{str(e)}")

def fire_action():
    if not FIRE_CONFIG["texts"]:
        messagebox.showwarning("警告", "请先设置开火文本！")
        return
    try:
        if FIRE_CONFIG["mode"] == 0:
            current_text = FIRE_CONFIG["texts"][FIRE_CONFIG["index"]]
            FIRE_CONFIG["index"] = (FIRE_CONFIG["index"] + 1) % len(FIRE_CONFIG["texts"])
        else:
            current_text = random.choice(FIRE_CONFIG["texts"])
        send_zh(current_text)
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x20, 0, 0, 0)
        time.sleep(0.1)
        ctypes.windll.user32.keybd_event(0x20, 0, 2, 0)
        print(f"🔥 开火成功！[{ '顺序' if FIRE_CONFIG['mode']==0 else '乱序' }] 文本：{current_text}")
        mode_label.config(text=f"当前模式：{ '顺序轮播' if FIRE_CONFIG['mode']==0 else '随机乱序' }")
    except Exception as e:
        messagebox.showwarning("开火失败", f"配置错误！\n错误：{str(e)}")

def save_fire_config():
    with open(FIRE_FILE, 'w', encoding='utf-8') as f:
        f.write(f"{FIRE_CONFIG['mode']} {' '.join(FIRE_CONFIG['texts'])}")

def load_fire_config():
    global FIRE_CONFIG
    try:
        if os.path.exists(FIRE_FILE):
            with open(FIRE_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    parts = content.split(" ", 1)
                    if len(parts) >= 2 and parts[0].isdigit():
                        FIRE_CONFIG["mode"] = int(parts[0])
                        FIRE_CONFIG["texts"] = [t.strip() for t in parts[1].split(" ") if t.strip()]
                        FIRE_CONFIG["index"] = 0
                    else:
                        FIRE_CONFIG = {"mode": 0, "texts": ["冲就完事了！", "这波我来Carry", "别白给！跟我上"], "index": 0}
                        save_fire_config()
    except Exception as e:
        FIRE_CONFIG = {"mode": 0, "texts": ["冲就完事了！", "这波我来Carry", "别白给！跟我上"], "index": 0}
        save_fire_config()

def set_fire_config():
    current_mode = "顺序" if FIRE_CONFIG["mode"] == 0 else "乱序"
    current_texts = " ".join(FIRE_CONFIG["texts"])
    prompt = f"格式：文本1 文本2 文本3（空格分隔）\n当前模式：{current_mode}\n示例：冲就完事了！ 这波我来Carry 别白给！跟我上"
    new_config = simpledialog.askstring("设置开火文本", prompt, initialvalue=current_texts)
    if new_config is not None:
        FIRE_CONFIG["texts"] = [t.strip() for t in new_config.split(" ") if t.strip()]
        save_fire_config()
        messagebox.showinfo("成功", f"已设置 {len(FIRE_CONFIG['texts'])} 条文本！")

def toggle_fire_mode():
    FIRE_CONFIG["mode"] = 1 - FIRE_CONFIG["mode"]
    mode_label.config(text=f"当前模式：{ '顺序轮播' if FIRE_CONFIG['mode']==0 else '随机乱序' }")
    save_fire_config()
    messagebox.showinfo("模式切换", f"已切换为 { '顺序轮播' if FIRE_CONFIG['mode']==0 else '乱序轮播' }")

# ===================== 文本管理 =====================
def load_msg():
    global MSG_LIST
    if os.path.exists(MSG_FILE):
        with open(MSG_FILE, 'r', encoding='utf-8') as f:
            MSG_LIST = [line.strip() for line in f if line.strip()] or MSG_LIST

def save_msg():
    with open(MSG_FILE, 'w', encoding='utf-8') as f:
        for msg in MSG_LIST:
            f.write(msg + "\n")

def add_msg():
    new_msg = simpledialog.askstring("添加文本", "输入要发送的内容：")
    if new_msg and new_msg.strip():
        MSG_LIST.append(new_msg.strip())
        save_msg()
        refresh_buttons()
        messagebox.showinfo("成功", f"已添加：{new_msg.strip()}")

def del_msg(msg):
    if messagebox.askyesno("删除确认", f"是否删除「{msg}」？"):
        MSG_LIST.remove(msg)
        save_msg()
        refresh_buttons()

def import_words():
    file_path = filedialog.askopenfilename(
        title="选择词汇文件（TXT）",
        filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_words = [line.strip() for line in f if line.strip()]
            if new_words:
                MSG_LIST.extend(new_words)
                MSG_LIST = list(set(MSG_LIST))
                save_msg()
                refresh_buttons()
                messagebox.showinfo("导入成功", f"导入 {len(new_words)} 条，总词汇数：{len(MSG_LIST)}")
            else:
                messagebox.showwarning("提示", "文件为空！")
        except Exception as e:
            messagebox.showerror("导入失败", f"错误：{str(e)}\n请确保文件为UTF-8编码")

# ===================== 新增：打开个人博客（修正弹窗提示） =====================
def open_blog():
    try:
        webbrowser.open("http://chukai.cc/")  # 正确的博客链接
        messagebox.showinfo("温馨提示", "欢迎来到初开的个人博客")  # 改为指定提示语
    except Exception as e:
        messagebox.showerror("失败", f"打开博客失败！\n错误：{str(e)}")

# ===================== 界面刷新（保留好看的UI） =====================
def refresh_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()
    for idx, msg in enumerate(MSG_LIST):
        btn_row = tk.Frame(button_frame, bg="#1a1a1a", bd=1, relief=tk.SOLID)
        btn_row.pack(fill=tk.X, pady=3, padx=2)

        # 发送按钮：保留好看的UI样式
        send_btn = tk.Button(
            btn_row, text=msg, bg="#333333", fg='white',
            font=("微软雅黑", 10, "bold"), relief=tk.RAISED,
            command=lambda x=msg: send_zh(x), bd=1, padx=10, pady=5
        )
        send_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)

        # 删除按钮：红色醒目
        del_btn = tk.Button(
            btn_row, text="删", bg="#ff4444", fg='white',
            font=("微软雅黑", 9, "bold"), relief=tk.RAISED,
            command=lambda x=msg: del_msg(x), bd=1, width=5
        )
        del_btn.pack(side=tk.RIGHT, padx=5, pady=2)

# ===================== 快捷键监听 =====================
def listen_hotkey():
    while True:
        if ctypes.windll.user32.GetAsyncKeyState(0x70) & 0x8000:
            root.withdraw() if root.state() == "normal" else root.deiconify()
            root.lift()
            time.sleep(0.5)
        if ctypes.windll.user32.GetAsyncKeyState(0x71) & 0x8000:
            fire_action()
            time.sleep(0.5)
        if ctypes.windll.user32.GetAsyncKeyState(0x1B) & 0x8000:
            if messagebox.askyesno("退出确认", "确定要退出吗？"):
                root.quit()
                sys.exit(0)
            time.sleep(0.5)
        time.sleep(0.01)

# ===================== 主界面（保留好看的UI+添加详细用法） =====================
# 主容器（纯颜色，Tkinter支持）
main_container = tk.Frame(root, bg="#222222", bd=2, relief=tk.GROOVE)
main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 标题栏（醒目+作者信息）
title_frame = tk.Frame(main_container, bg="#333333", bd=2, relief=tk.SOLID)
title_frame.pack(fill=tk.X, pady=10, padx=10)

title_label = tk.Label(
    title_frame, text="CS2工具箱",
    font=("微软雅黑", 22, "bold"), bg="#333333", fg='#00ffff'
)
title_label.pack(pady=5)

# 作者信息
author_label = tk.Label(
    title_frame, text="作者：初开",
    font=("微软雅黑", 10), bg="#333333", fg='white'
)
author_label.pack()

# 详细用法说明（新增）
usage_label = tk.Label(
    title_frame, 
    text="📖 使用说明：\n1. F1：显示/隐藏窗口 | 2. F2：一键发送开火文本 | 3. ESC：退出程序\n4. 点击文本按钮直接发送 | 5. 可自定义开火文本和添加常用话术",
    font=("微软雅黑", 9), bg="#333333", fg='#dddddd', justify=tk.LEFT
)
usage_label.pack(pady=5, padx=10)

# 功能按钮区（大按钮，容易点）
func_frame = tk.Frame(main_container, bg="#222222")
func_frame.pack(fill=tk.X, pady=10)

# 开火功能区
fire_frame = tk.Frame(main_container, bg="#222222", bd=2, relief=tk.SOLID)
fire_frame.pack(fill=tk.X, pady=10, padx=10)

mode_label = tk.Label(
    fire_frame, text="当前模式：顺序轮播",
    font=("微软雅黑", 10), bg="#333333", fg='white'
)
mode_label.pack(pady=5)

fire_btn_frame = tk.Frame(fire_frame, bg="#222222")
fire_btn_frame.pack(pady=10)

tk.Button(
    fire_btn_frame, text="设置开火文本", bg="#444444", fg='white',
    font=("微软雅黑", 10), relief=tk.RAISED, command=set_fire_config,
    bd=2, padx=15, pady=5
).pack(side=tk.LEFT, padx=5)

tk.Button(
    fire_btn_frame, text="切换轮播模式", bg="#444444", fg='white',
    font=("微软雅黑", 10), relief=tk.RAISED, command=toggle_fire_mode,
    bd=2, padx=15, pady=5
).pack(side=tk.LEFT, padx=5)

tk.Button(
    fire_btn_frame, text="一键开火 (F2)", bg="#ff4444", fg='white',
    font=("微软雅黑", 10, "bold"), relief=tk.RAISED, command=fire_action,
    bd=2, padx=20, pady=5
).pack(side=tk.LEFT, padx=5)

# 文本管理区
text_manage_frame = tk.Frame(main_container, bg="#222222", bd=2, relief=tk.SOLID)
text_manage_frame.pack(fill=tk.X, pady=10, padx=10)

tk.Button(
    text_manage_frame, text="添加自定义文本", bg="#444444", fg='white',
    font=("微软雅黑", 10), relief=tk.RAISED, command=add_msg,
    bd=2, padx=15, pady=5
).pack(side=tk.LEFT, padx=10, pady=10)

tk.Button(
    text_manage_frame, text="一键导入词汇", bg="#444444", fg='white',
    font=("微软雅黑", 10), relief=tk.RAISED, command=import_words,
    bd=2, padx=15, pady=5
).pack(side=tk.LEFT, padx=10, pady=10)

# 个人博客按钮（白色样式）
blog_btn = tk.Button(
    text_manage_frame, text="🔗 我的博客 chukai.cc", bg="white", fg="#000000",  # 白色背景+黑色文字
    font=("微软雅黑", 10, "bold"), relief=tk.RAISED, command=open_blog,
    bd=2, padx=15, pady=5
)
blog_btn.pack(side=tk.LEFT, padx=10, pady=10)

# 文本列表区（滚动+清晰可见）
scroll_frame = tk.Frame(main_container, bg="#222222")
scroll_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

scrollbar = ttk.Scrollbar(scroll_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

button_canvas = tk.Canvas(scroll_frame, yscrollcommand=scrollbar.set, bg="#333333")
button_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=button_canvas.yview)

inner_frame = tk.Frame(button_canvas, bg="#333333")
button_canvas.create_window((0, 0), window=inner_frame, anchor="nw")
inner_frame.bind("<Configure>", lambda e: button_canvas.configure(scrollregion=button_canvas.bbox("all")))
button_frame = inner_frame

# 底部快捷键提示（强化）
guide_label = tk.Label(
    main_container, text="⌨️ 快捷键汇总：F1显隐 | F2开火 | ESC退出",
    font=("微软雅黑", 10, "bold"), bg="#222222", fg='#00ffff'
)
guide_label.pack(side=tk.BOTTOM, pady=8)

# ===================== 初始化 =====================
if __name__ == "__main__":
    try:
        import pyperclip
        from PIL import Image, ImageTk
    except ImportError as e:
        missing_lib = str(e).split()[-1]
        os.system(f"pip install {missing_lib} -i https://pypi.tuna.tsinghua.edu.cn/simple")
        import pyperclip
        import webbrowser  # 确保导入博客相关库
        from PIL import Image, ImageTk
    
    load_msg()
    load_fire_config()
    refresh_buttons()
    
    hotkey_thread = threading.Thread(target=listen_hotkey, daemon=True)
    hotkey_thread.start()
    
    root.mainloop()
