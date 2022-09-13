#
# CanvasAreaSettingWindow.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk
from tkinter.messagebox import showwarning
from contents.Constants import messages


# メインウィンドウのカンバス部分の設定ウィンドウのクラス
class CanvasAreaSettingWindow(tk.Toplevel):
    def __init__(self, master):
        # ポップアップ・ウィンドウの初期化
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.title(messages["settings_title"])
        self.resizable(False, False)

        # StringVar
        # カンバス・グリッドの変数
        self.var_canvas_grid = tk.StringVar(value=str(self.master.canvas.var_canvas_grid.get()))
        # カンバス座標の変数
        self.var_canvas_x = tk.StringVar(value=str(self.master.canvas.var_canvas_x.get()))
        self.var_canvas_y = tk.StringVar(value=str(self.master.canvas.var_canvas_y.get()))
        # カンバス・サイズの変数
        self.var_canvas_x_pixel = tk.StringVar(value=str(self.master.canvas.var_canvas_x_pixel.get()))
        self.var_canvas_y_pixel = tk.StringVar(value=str(self.master.canvas.var_canvas_y_pixel.get()))

        # Label
        # カンバス・グリッドのラベル
        self.label_grid = tk.Label(self, text=messages["canvas_grid_label"])
        # カンバス・サイズのラベル
        self.label_frame_size = tk.Label(self, text=messages["canvas_frame_size_label"])
        # カンバス座標のラベル
        self.label_resolution = tk.Label(self, text=messages["canvas_resolution_label"])

        # Entry
        # カンバス・グリッドのテキストボックス
        self.entry_canvas_grid = tk.Entry(self, textvariable=self.var_canvas_grid, font=14, width=7)
        # カンバス座標のテキストボックス
        self.entry_canvas_x = tk.Entry(self, textvariable=self.var_canvas_x, font=14, width=7)
        self.entry_canvas_y = tk.Entry(self, textvariable=self.var_canvas_y, font=14, width=7)
        # カンバス・サイズのテキストボックス
        self.entry_canvas_x_pixel = tk.Entry(self, textvariable=self.var_canvas_x_pixel, font=14, width=7)
        self.entry_canvas_y_pixel = tk.Entry(self, textvariable=self.var_canvas_y_pixel, font=14, width=7)

        # Frame
        # ボタンのフレーム
        self.btn_frame = tk.Frame(self)
        self.btn_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")

        # Button
        # Okボタン
        self.btn_ok = tk.Button(self.btn_frame, text=messages["ok_button"], command=self.ok)
        # キャンセル・ボタン
        self.btn_cancel = tk.Button(self.btn_frame, text=messages["cancel_button"], command=self.cancel)

        # ラベルの配置
        self.label_frame_size.grid(row=0, column=0, padx=10, pady=(10, 0))
        self.label_resolution.grid(row=1, column=0, padx=10)
        self.label_grid.grid(row=2, column=0, padx=10)
        # テキストボックスの配置
        self.entry_canvas_x_pixel.grid(row=0, column=1, pady=(10, 0))
        self.entry_canvas_y_pixel.grid(row=0, column=2, padx=(0, 10), pady=(10, 0))
        self.entry_canvas_x.grid(row=1, column=1)
        self.entry_canvas_y.grid(row=1, column=2, padx=(0, 10))
        self.entry_canvas_grid.grid(row=2, column=1)
        # ボタン・フレームの配置
        self.btn_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W + tk.E, padx=10, pady=10)
        self.btn_ok.grid(row=0, column=0, sticky=tk.W + tk.E, padx=(40, 20))
        self.btn_cancel.grid(row=0, column=1, sticky=tk.W + tk.E, padx=(20, 40))

        # コマンドのバインド
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    # Okコマンド
    def ok(self, *event):
        # テキストボックス入力値の取得
        canvas_grid = self.var_canvas_grid.get()
        canvas_x = self.var_canvas_x.get()
        canvas_y = self.var_canvas_y.get()
        canvas_x_pixel = self.var_canvas_x_pixel.get()
        canvas_y_pixel = self.var_canvas_y_pixel.get()

        # テキストボックス入力値が数値であるかの確認
        if not (canvas_x_pixel.isdigit() and canvas_y_pixel.isdigit() and canvas_x.isdigit() and
                canvas_y.isdigit() and canvas_grid.isdigit()):
            showwarning(title=messages["warning_title"], message=messages["input_error"])
            return

        # テキストボックス入力値を数値への変換
        canvas_x = int(canvas_x)
        canvas_y = int(canvas_y)
        canvas_x_pixel = int(canvas_x_pixel)
        canvas_y_pixel = int(canvas_y_pixel)
        canvas_grid = int(canvas_grid)

        # カンバスのテキストボックス入力値がゼロでないかの確認
        if not (canvas_x_pixel > 0 and canvas_y_pixel > 0 and
                canvas_x > 0 and canvas_y > 0):
            showwarning(title=messages["warning_title"], message=messages["input_error"])
            return

        # テキストボックス入力値をメイン・アプリに設定
        self.master.canvas.var_canvas_grid.set(canvas_grid)
        self.master.canvas.var_canvas_x.set(canvas_x)
        self.master.canvas.var_canvas_y.set(canvas_y)
        self.master.canvas.var_canvas_x_pixel.set(canvas_x_pixel)
        self.master.canvas.var_canvas_y_pixel.set(canvas_y_pixel)

        # ポップアップ・ウィンドウを閉じる
        self.destroy()

    # キャンセル・コマンド
    def cancel(self, *event):
        # ポップアップ・ウィンドウを閉じる
        self.destroy()
