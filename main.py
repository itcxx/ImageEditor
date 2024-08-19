import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def resize_image(input_image_path, output_image_path, min_size=(295, 414), max_kb=200):
    try:
        with Image.open(input_image_path) as img:
            width, height = img.size

            # 检查并调整图像的最小尺寸
            if width < min_size[0] or height < min_size[1]:
                ratio_w = min_size[0] / width
                ratio_h = min_size[1] / height
                ratio = max(ratio_w, ratio_h)
                new_size = (int(width * ratio), int(height * ratio))
                img = img.resize(new_size, Image.LANCZOS)

            # 保存初次调整后的图像并检查文件大小
            quality = 95
            img.save(output_image_path, format='JPEG', quality=quality)

            # 如果文件大小超过限制，逐步降低质量
            while os.path.getsize(output_image_path) > max_kb * 1024 and quality > 10:
                quality -= 5
                img.save(output_image_path, format='JPEG', quality=quality)

        return True
    except Exception as e:
        print(f"Error occurred during image processing: {e}")
        return False


def select_file():
    file_path = filedialog.askopenfilename(title="选择要转换的图片文件")
    if file_path:
        # 获取原始文件名，不带路径
        original_file_name = os.path.basename(file_path)

        # 使用原始文件名作为默认的保存文件名
        output_file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            title="保存转换后的图片",
            initialfile=original_file_name
        )

        if output_file_path:
            try:
                progress_label.config(text="正在转换中...")
                resize_image(file_path, output_file_path)
                progress_label.config(text="转换完成")
                messagebox.showinfo("完成", f"图片已成功转换并保存为 {output_file_path}")
            except Exception as e:
                progress_label.config(text="转换失败")
                messagebox.showerror("错误", f"处理图片时发生错误：{str(e)}")


def select_folder():
    folder_path = filedialog.askdirectory(title="选择包含要转换图片的文件夹")
    if folder_path:
        save_folder_path = filedialog.askdirectory(title="选择保存转换后图片的文件夹")
        if save_folder_path:
            try:
                progress_label.config(text="正在转换中...")
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                            progress_label.config(text=f"正在转换中...{file}")
                            input_image_path = os.path.join(root, file)
                            output_image_path = os.path.join(save_folder_path, f"{file}")
                            resize_image(input_image_path, output_image_path)
                progress_label.config(text="转换完成")
                messagebox.showinfo("完成", "所有图片均已成功转换")
            except Exception as e:
                progress_label.config(text="转换失败")
                messagebox.showerror("错误", f"处理图片时发生错误：{str(e)}")

def display_qr_code_image(qr_image_path):
    qr_img = Image.open(qr_image_path)
    qr_img = qr_img.resize((150, 150))  # 调整二维码图片大小
    qr_img_tk = ImageTk.PhotoImage(qr_img)
    qr_label.config(image=qr_img_tk)
    qr_label.image = qr_img_tk  # 防止图片被垃圾回收

def resource_path(relative_path):
    """获取资源文件的绝对路径，适应打包后的路径结构"""
    try:
        # PyInstaller创建临时文件夹，并将路径存储于 _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# 创建主窗口
root = tk.Tk()
root.title("图片大小转换工具")
root.geometry("500x400")
# 顶部框架用于显示应用说明
top_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="groove")
top_frame.pack(fill="x", padx=10, pady=10)

# 应用说明标签
app_description = tk.Label(top_frame,
                           text="!!!  此工具用于将图片调整到小于200KB且尺寸不小于295x413像素  !!!",
                           fg="blue",
                           bg="#f0f0f0",
                           font=("Arial", 10, "bold"),
                           pady=10, padx=10)
app_description.pack()

# 在说明下面添加一条分隔线
separator = tk.Frame(root, height=2, bd=1, relief="sunken")
separator.pack(fill="x", padx=5, pady=5)


# 主框架，用于放置按钮和二维码图片
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# 左侧按钮框架
button_frame = tk.Frame(main_frame)
button_frame.pack(side="left", padx=20, pady=20)

# 右侧图片框架
qr_frame = tk.Frame(main_frame)
qr_frame.pack(side="right", padx=20, pady=20)

# 添加按钮到左侧
file_button = tk.Button(button_frame, text="选择单个图片文件转换", command=select_file)
file_button.pack(pady=10)

folder_button = tk.Button(button_frame, text="选择文件夹转换(将会转换文件夹中所有的图片)", command=select_folder)
folder_button.pack(pady=10)

# 添加提示文本
progress_label = tk.Label(button_frame, text="", fg="blue")
progress_label.pack(pady=10)

# 在右侧显示二维码的图片框
qr_label = tk.Label(qr_frame)
qr_label.pack()

# 显示文字
text = tk.Label(qr_frame, text ="求打赏: \n 一万不嫌多 一块不嫌少" ,fg="red")
text.pack()

# 显示现有的二维码图片
qr_image_path =  resource_path('resources/pay.png') # 替换为你的二维码图片路径
display_qr_code_image(qr_image_path)

# 底部框架用于显示版权声明
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill="x", padx=10, pady=5)

# 版权声明标签
copyright_label = tk.Label(bottom_frame, text="© 2024 itcxx. All rights reserved.", fg="black", font=("Arial", 8))
copyright_label.pack()

# 运行主循环
root.mainloop()
# # 创建主窗口
