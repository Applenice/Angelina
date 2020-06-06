import os
import sys
import zipfile
import hashlib
import tkinter as tk
from tkinter import ttk, HORIZONTAL, IntVar
from tkinter import filedialog


class Angelina:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Angelina')

        self.exec_path = os.path.dirname(sys.path[0])
        self.window.iconbitmap(self.exec_path + r'\Angelina.ico')
        self.progress_bar = ttk.Progressbar(self.window, orient=HORIZONTAL, length=190, mode='determinate')

        self.aim_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.input_password_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.progress_var = tk.StringVar()
        self.progress_var.set('0%')

        self.rename = IntVar()
        self.frm = tk.Frame(self.window, padx=5, pady=5)
        self.app()

    def app(self):
        tk.Label(self.window, text="选择输入目录:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(self.window, textvariable=self.aim_path_var).grid(row=0, column=1)
        tk.Button(self.window, text="目录选择",
                  command=self.select_input_dir).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.window, text="选择输出目录:").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(self.window, textvariable=self.output_path_var).grid(row=1, column=1)
        tk.Button(self.window, text="目录选择",
                  command=self.select_output_dir).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self.window, text="批量解压密码:").grid(row=2, column=0, sticky=tk.W)
        tk.Entry(self.window, textvariable=self.input_password_var).grid(row=2, column=1)
        tk.Button(self.window, text="确认密码",
                  command=self.set_password).grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self.window, text="输出文件更名:").grid(row=3, column=0, sticky=tk.W)
        checkbutton = tk.Checkbutton(self.frm, text='MD5', variable=self.rename)
        checkbutton.grid(row=3, column=1, padx=5, pady=5)
        self.frm.grid(row=3, column=1)

        tk.Label(self.window, text="当前执行进度:").grid(row=4, column=0, sticky=tk.W)
        self.progress_bar.grid(row=4, column=1, padx=5, pady=5)
        tk.Label(self.window, textvariable=self.progress_var).grid(row=4, column=2, sticky=tk.W)

        tk.Button(self.window, text="批量解压", width=20, height=1,
                  command=self.batch_uncompress).grid(row=5, column=1, padx=5, pady=5)

    def init_progress(self):
        self.progress_var.set('0%')
        self.progress_bar["value"] = 0
        self.progress_bar.update()

    def select_input_dir(self):
        file_name = filedialog.askdirectory(title='选择输入目录', initialdir='./')
        self.aim_path_var.set(file_name)
        self.init_progress()

    def select_output_dir(self):
        file_name = filedialog.askdirectory(title='选择输出目录', initialdir='./')
        self.output_path_var.set(file_name)
        self.init_progress()

    def set_password(self):
        self.password_var.set("{}".format(self.input_password_var.get()))
        self.init_progress()

    def batch_uncompress(self):
        password = self.password_var.get()
        input_dir = self.aim_path_var.get() + '/'
        output_dir = self.output_path_var.get() + '/'

        if input_dir == '/' or output_dir == '/':
            self.progress_var.set('未选目录!')
            self.progress_bar.update()
        else:
            file_list = os.listdir(input_dir)
            file_count = len(file_list)
            self.progress_bar["maximum"] = file_count
            succeed = 0

            try:
                for sub_file_name in file_list:
                    zip_file = zipfile.ZipFile(input_dir + sub_file_name)
                    for names in zip_file.namelist():
                        zip_file.extract(names, output_dir, pwd=bytes(password, encoding="utf8"))
                        if self.rename.get() == 1:
                            with open(output_dir + names, 'rb') as fin:
                                file_md5 = hashlib.md5(fin.read()).hexdigest()
                            os.rename(output_dir + names, output_dir + file_md5)
                    zip_file.close()
                    succeed += 1
                    self.progress_bar["value"] = succeed
                    self.progress_var.set('{:.2f}%'.format(succeed / file_count * 100))
                    self.progress_bar.update()
            except RuntimeError:
                self.progress_var.set('密码错误')
                self.progress_bar.update()
            except zipfile.BadZipFile:
                self.progress_var.set('非ZIP文件')
                self.progress_bar.update()
            except Exception:
                self.progress_var.set('未知错误')
                self.progress_bar.update()


if __name__ == '__main__':
    root = Angelina()
    root.window.mainloop()
