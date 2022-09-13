#
# MainWindow.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk
from tkinter.messagebox import askyesno
from contents.CanvasArea import CanvasArea
from contents.Settings import Settings
from contents.ListBoxOperation import ListBoxOperation
from contents.Click import Click
from contents.DrawingProcessing import DrawingProcessing
from contents.IO import IO
from contents.PointOperation import PointOperation
from contents.MainWindowArrangement import MainWindowArrangement
from contents.CommandBind import CommandBind
from contents.Constants import (
    messages, CONFIRMATION_TITLE, CONFIRMATION_MESSAGE,
    UNSAVED_CHANGES_MESSAGE, OPTIONS_POS, OPTIONS_PREVIEW
)


# メイン・ウィンドウのクラス
class MainWindow(tk.Frame, Settings, ListBoxOperation, Click, DrawingProcessing, IO,
                 PointOperation, MainWindowArrangement, CommandBind):
    def __init__(self, master):
        # メイン・ウィンドウの初期化
        super().__init__(master)
        self.master = master
        self.master.title(messages["main_title"])
        self.master.resizable(False, False)

        # 保存フラグ
        self.saved = True

        # IntVar
        self.init_intvar()

        # StringVar
        self.init_strvar()

        # Canvas
        self.canvas = CanvasArea(self)

        # Menu
        self.menubar = tk.Menu(self.master)

        # メニューコマンドのバインド
        self.menu_command_bind()

        # UIパーツの配置
        self.ui_arrangement()

        # キーコマンドのバインド
        self.key_command_bind()

        # メニューの設定
        self.master.config(menu=self.menubar)

        # History
        self.clear_history()

        # 表示
        self.draw_everything()

        # フォルダ構成の確認
        self.check_file_arrangement()

    # メイン・アプリを終了する
    def quit(self, *event):
        if not self.saved:
            answer = askyesno(title=CONFIRMATION_TITLE,
                              message=UNSAVED_CHANGES_MESSAGE + "\n" + CONFIRMATION_MESSAGE)
            if not answer:
                return

        self.master.destroy()

    # 数値変数の初期化
    def init_intvar(self):
        # 多角形ループの変数(bool)
        self.var_loop = tk.IntVar()
        # 多角形反転の変数(bool)
        self.var_reverse_y = tk.IntVar()
        # 座標丸めの変数
        self.var_round = tk.IntVar(value=3)
        self.var_type_tangents = tk.IntVar(value=1)

    # 文字列変数の初期化
    def init_strvar(self):
        # 座標原点の変数
        self.var_origin = tk.StringVar(value=OPTIONS_POS[0])
        # 多角形パスの変数
        self.var_poly_path = tk.StringVar()
        # 操作プレビューの変数
        self.var_preview = tk.StringVar(value=OPTIONS_PREVIEW[0])
        # テキストボックスの座標の変数
        self.var_entry_x = tk.StringVar()
        self.var_entry_y = tk.StringVar()
