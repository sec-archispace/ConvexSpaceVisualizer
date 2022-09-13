#
# IO.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import os
import csv
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import askyesno, showwarning
from contents.Constants import (
    messages, INPUT_FOLDER, CONVEXSPACEHEATMAP_FOLDER, CONVEXSPACEHEATMAP_INPUT_FILE,
    CONVEXSPACEHEATMAP_OUTPUT_FILE, CONFIRMATION_TITLE, CONFIRMATION_MESSAGE,
    UNSAVED_CHANGES_MESSAGE, OVERWRITE_MESSAGE, OPTIONS_POS, CONVEXSPACEHEATMAP_EPROPERTIES_FILE,
    CONVEXSPACEHEATMAP_JAR_FILE
)


# 入出力処理のクラス
class IO:

    # リストボックスでの多角形の座標をcsvファイルに保存
    def save_to_csv_file(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()

        try:
            f = open(self.var_poly_path.get(), "w", newline="")
            writer = csv.writer(f, delimiter=",")
            for listbox_entry_x, listbox_entry_y in zip(self.listbox_x.get(0, tk.END), self.listbox_y.get(0, tk.END)):
                writer.writerow([listbox_entry_x, listbox_entry_y])
        except Exception as e:
            print(e)
            showwarning(title=messages["warning_title"], message=messages["cannot_overwrite_input_file"])

    # リストボックスでの多角形の座標を開いたファイルに保存
    def save(self, *event):
        if not self.var_poly_path.get():
            self.save_as()
            return

        self.save_to_csv_file()
        self.saved = True

    # リストボックスでの多角形の座標を選定のファイルに保存
    def save_as(self, *event):
        fTyp = [("vertex_lists", "*.csv")]
        file_name = filedialog.asksaveasfilename(initialdir=f"./{INPUT_FOLDER}/",
                                                 filetypes=fTyp, defaultextension=".csv")
        if file_name:
            self.var_poly_path.set(file_name)
        else:
            return

        self.save()

    # 多角形の座標をcsvファイルからリストボックスにロード
    def load_from_csv_file(self, *event):
        self.listbox_x.delete(0, tk.END)
        self.listbox_y.delete(0, tk.END)

        with open(self.var_poly_path.get(), "r", newline="") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                self.listbox_x.insert(tk.END, f"{row[0]}")
                self.listbox_y.insert(tk.END, f"{row[1]}")

    # 多角形の座標を選定のファイルからリストボックスにロード
    def load(self, *event):
        if not self.saved:
            answer = askyesno(title=CONFIRMATION_TITLE,
                              message=UNSAVED_CHANGES_MESSAGE + "\n" + CONFIRMATION_MESSAGE)
            if not answer:
                return
        fTyp = [("vertex_lists", "*.csv")]
        file_name = filedialog.askopenfilename(initialdir=f"./{INPUT_FOLDER}/", filetypes=fTyp)
        if file_name:
            self.var_poly_path.set(file_name)
        else:
            return

        self.load_from_csv_file()
        self.saved = True

        self.clear_history()

        self.draw_everything()

    # 画像をファイルからロード
    def load_background_image(self, *event):
        self.canvas.load_background_image()

        self.draw_everything()

    # 画像を生成
    def generate_background_image(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        if self.listbox_x.size() < 3:
            showwarning(title=messages["warning_title"], message=messages["lack_points"])
            return
        answer = askyesno(title=CONFIRMATION_TITLE,
                          message=OVERWRITE_MESSAGE + "\n" + CONFIRMATION_MESSAGE)
        if not answer:
            return

        if os.path.exists(f"./{CONVEXSPACEHEATMAP_OUTPUT_FILE}"):
            os.remove(f"./{CONVEXSPACEHEATMAP_OUTPUT_FILE}")

        poly_path_backup = self.var_poly_path.get()
        self.var_poly_path.set(f"./{CONVEXSPACEHEATMAP_INPUT_FILE}")
        self.save_to_csv_file()
        self.var_poly_path.set(poly_path_backup)

        wd = os.getcwd()
        os.chdir(wd + rf"/{CONVEXSPACEHEATMAP_FOLDER}")
        result = subprocess.run([r"java", r"-jar", r"convexspaceheatmap.jar"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if result.returncode != 0:
            try:
                showwarning(title=messages["warning_title"], message=result.stdout.decode('utf-8'))
            except Exception as e:
                print(e)
                showwarning(title=messages["warning_title"], message=result.stdout.decode('shift_jis'))
            os.chdir(wd)
            return
        else:
            try:
                print(result.stdout.decode('utf-8'))
            except Exception as e:
                print(e)
                print(result.stdout.decode('shift_jis'))
        os.chdir(wd)

        if not os.path.exists(f"./{CONVEXSPACEHEATMAP_OUTPUT_FILE}"):
            showwarning(title=messages["warning_title"], message=messages["gen_image_error"])
            return

        self.canvas.var_image_background_path.set(f"./{CONVEXSPACEHEATMAP_OUTPUT_FILE}")
        self.canvas.load_background_image_from_file()
        self.backgroundmenu.entryconfig(messages["show_image"], state="normal")
        self.canvas.var_show_background.set(1)
        if self.var_origin.get() == OPTIONS_POS[0]:
            self.canvas.var_image_flip.set(0)
        else:
            self.canvas.var_image_flip.set(1)
        self.canvas.var_image_pos.set(self.var_origin.get())

        self.draw_everything()

    # ファイル配置のチェック
    def check_file_arrangement(self):
        epropeties_file = True
        jar_file = True
        warning_message = ""
        if not os.path.exists(f"./{CONVEXSPACEHEATMAP_EPROPERTIES_FILE}"):
            warning_message += messages["cannot_open_eproperties_file"]
            epropeties_file = False
        if not os.path.exists(f"./{CONVEXSPACEHEATMAP_JAR_FILE}"):
            warning_message += messages["cannot_open_jar_file"]
            jar_file = False
        if epropeties_file and jar_file:
            return
        else:
            showwarning(title=messages["warning_title"], message=warning_message)
