#
# HeatMapConfigWindow.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import os
import shutil
import tkinter as tk
from tkinter.messagebox import showwarning
from contents.Utils import is_float
from contents.Constants import messages, CONVEXSPACEHEATMAP_EPROPERTIES_FILE


# ヒートマップ生成条件の設定ウィンドウのクラス
class HeatMapConfigWindow(tk.Toplevel):
    def __init__(self, master):
        # ポップアップ・ウィンドウの初期化
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.title(messages["settings_title"])
        self.resizable(False, False)

        # IntVar
        self.var_type_tangents = tk.IntVar(value=1)

        # StringVar
        self.var_number_tangents = tk.StringVar()
        self.var_angle_tangents = tk.StringVar()
        self.var_weight_coefficient = tk.StringVar()

        # Radiobutton
        self.radio_number_tangents = tk.Radiobutton(self, text=messages["num_tangents"],
                                                    value=1, variable=self.var_type_tangents)
        self.radio_angle_tangents = tk.Radiobutton(self, text=messages["ang_tangents"],
                                                   value=2, variable=self.var_type_tangents)

        # Label
        self.label_weight_coefficient = tk.Label(self, text=f"{' ':7}{messages['weight_coeff']}")

        # Entry
        self.entry_number_tangents = tk.Entry(self, textvariable=self.var_number_tangents, font=14, width=7)
        self.entry_angle_tangents = tk.Entry(self, textvariable=self.var_angle_tangents, font=14, width=7)
        self.entry_angle_tangents.config(state='disabled')
        self.entry_weight_coefficient = tk.Entry(self, textvariable=self.var_weight_coefficient, font=14, width=7)

        # Frame
        # ボタンのフレーム
        self.btn_frame = tk.Frame(self)
        self.btn_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")

        # Button
        # 画像生成のボタン
        self.btn_gen_image = tk.Button(self, text=messages["gen_image"], command=self.generate_background_image)
        # Okボタン
        self.btn_ok = tk.Button(self.btn_frame, text=messages["ok_button"], command=self.ok)
        # キャンセル・ボタン
        self.btn_cancel = tk.Button(self.btn_frame, text=messages["cancel_button"], command=self.cancel)

        # ラベルの配置
        self.radio_number_tangents.grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 0))
        self.radio_angle_tangents.grid(row=1, column=0, sticky=tk.W, padx=10, pady=(0, 10))
        self.label_weight_coefficient.grid(row=2, column=0, sticky=tk.W, padx=10, pady=(0, 10))
        # テキストボックスの配置
        self.entry_number_tangents.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))
        self.entry_angle_tangents.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))
        self.entry_weight_coefficient.grid(row=2, column=1, padx=(0, 10), pady=(0, 10))
        # ボタン・フレームの配置
        self.btn_gen_image.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10))
        self.btn_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W + tk.E, padx=10, pady=(0, 10))
        self.btn_ok.grid(row=0, column=0, sticky=tk.W + tk.E, padx=(30, 15))
        self.btn_cancel.grid(row=0, column=1, sticky=tk.W + tk.E, padx=(15, 30))

        # コマンドのバインド
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.var_type_tangents.trace("w", self.update_type_tangents)

        self.backup_properties()
        self.read_properties()

    # 接線種類更新
    def update_type_tangents(self, *event):
        value = self.var_type_tangents.get()

        if value == 1:
            self.entry_number_tangents.config(state='normal')
            self.entry_angle_tangents.config(state='disabled')
        elif value == 2:
            self.entry_number_tangents.config(state='disabled')
            self.entry_angle_tangents.config(state='normal')

    # 設定ファイルをバックアップ
    def backup_properties(self, *event):
        try:
            shutil.copy2(CONVEXSPACEHEATMAP_EPROPERTIES_FILE, CONVEXSPACEHEATMAP_EPROPERTIES_FILE + "_backup")
        except Exception as e:
            print(e)
            showwarning(title=messages["warning_title"], message=messages["cannot_backup_eproperties_file"])

    # バックアップファイルを削除
    def remove_backup(self, *event):
        os.remove(CONVEXSPACEHEATMAP_EPROPERTIES_FILE + "_backup")

    # バックアップファイルを回復
    def restore_backup(self, *event):
        try:
            shutil.copy2(CONVEXSPACEHEATMAP_EPROPERTIES_FILE + "_backup", CONVEXSPACEHEATMAP_EPROPERTIES_FILE)
        except Exception as e:
            print(e)
            showwarning(title=messages["warning_title"], message=messages["cannot_write_eproperties_file"])

    # 設定ファイルを読み込む
    def read_properties(self, *event):
        self.properties = []
        try:
            f = open(CONVEXSPACEHEATMAP_EPROPERTIES_FILE, encoding='utf-8')
            for line in f:
                self.properties.append(line)

                if line.startswith("number_tangents="):
                    value = line.split("=")[1].rstrip()
                    self.var_number_tangents.set(value)
                elif line.startswith("angle_tangents="):
                    value = line.split("=")[1].rstrip()
                    self.var_angle_tangents.set(value)
                elif line.startswith("type_tangents="):
                    value = line.split("=")[1].rstrip()
                    if value in ("1", "2"):
                        self.var_type_tangents.set(int(value))
                elif line.startswith("weight_coefficient="):
                    value = line.split("=")[1].rstrip()
                    self.var_weight_coefficient.set(value)
        except Exception as e:
            print(e)
            showwarning(title=messages["warning_title"], message=messages["cannot_read_eproperties_file"])

    # 設定ファイルを出力
    def write_properties(self, *event):
        number_tangents = self.var_number_tangents.get()
        angle_tangents = self.var_angle_tangents.get()
        type_tangents = self.var_type_tangents.get()
        weight_coefficient = self.var_weight_coefficient.get()

        number_tangents_written = False
        angle_tangents_written = False
        type_tangents_written = False
        weight_coefficient_written = False

        if not (number_tangents.isdigit() and is_float(angle_tangents) and
                float(angle_tangents) > 0 and is_float(weight_coefficient) and
                float(weight_coefficient) > 0):
            showwarning(title=messages["warning_title"], message=messages["input_error"])
            return -1

        try:
            f = open(CONVEXSPACEHEATMAP_EPROPERTIES_FILE, 'w', encoding='utf-8')
            for line in self.properties:
                if line.startswith("number_tangents="):
                    f.write("number_tangents=" + number_tangents + "\n")
                    type_tangents_written = True
                elif line.startswith("angle_tangents="):
                    f.write("angle_tangents=" + angle_tangents + "\n")
                    number_tangents_written = True
                elif line.startswith("type_tangents="):
                    f.write("type_tangents=" + str(type_tangents) + "\n")
                    angle_tangents_written = True
                elif line.startswith("weight_coefficient="):
                    f.write("weight_coefficient=" + str(weight_coefficient) + "\n")
                    weight_coefficient_written = True
                else:
                    f.write(line)
        except Exception as e:
            print(e)
            showwarning(title=messages["warning_title"], message=messages["cannot_write_eproperties_file"])

            if not number_tangents_written:
                f.write("number_tangents=" + number_tangents + "\n")
            if not angle_tangents_written:
                f.write("angle_tangents=" + angle_tangents + "\n")
            if not type_tangents_written:
                f.write("type_tangents=" + str(type_tangents) + "\n")
            if not weight_coefficient_written:
                f.write("weight_coefficient=" + str(weight_coefficient) + "\n")

        return 0

    # 画像を生成
    def generate_background_image(self, *event):
        result = self.write_properties()
        if result == -1:
            return

        self.master.generate_background_image()

    # Okコマンド
    def ok(self, *event):
        result = self.write_properties()
        if result == -1:
            return

        self.remove_backup()

        # ポップアップ・ウィンドウを閉じる
        self.destroy()

    # キャンセル・コマンド
    def cancel(self, *event):
        self.restore_backup()
        self.remove_backup()

        # ポップアップ・ウィンドウを閉じる
        self.destroy()
