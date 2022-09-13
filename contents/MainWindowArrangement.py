#
# MainWindowArrangement.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk
from contents.Constants import messages


# メインウィンドウのUI配置のクラス
class MainWindowArrangement:
    def ui_arrangement(self):
        # Frame
        self.set_frame()

        # ウィジェット・フレームの配置
        self.frame.pack(side=tk.LEFT, padx=(0, 40), pady=40)

        # Button
        self.set_button()

        # Entry
        self.set_entry()

        # Listbox
        self.set_list_box()

        # Menu
        self.menu_arrangement()

    # Frameの初期化
    def set_frame(self):
        # ウィジェットのフレーム
        self.frame = tk.Frame(self.master)
        # ウィジェットのフレーム
        self.entry_frame = tk.Frame(self.frame)
        # ボタンのフレーム
        self.btn_frame = tk.Frame(self.frame)
        # リストボックスのフレーム
        self.listbox_frame = tk.Frame(self.frame)

    # Buttonの初期化
    def set_button(self):
        # 点追加のボタン
        self.btn_add = tk.Button(self.btn_frame, text=u"\u002B", command=self.add, font=("Arial", "14"), width=2)
        # 点変換のボタン
        self.btn_replace = tk.Button(self.btn_frame, text=u"\u21F5",
                                     command=self.replace, font=("Arial", "14"), width=2)
        # 点削除のボタン
        self.btn_delete = tk.Button(self.listbox_frame, text=u"\U0001F5D1",
                                    command=self.delete, font=("Arial", "14"), width=1)
        # 点前後のボタン
        self.btn_move_down = tk.Button(self.listbox_frame, text=u"\u2193",
                                       command=self.move_down, font=("Arial", "14"), width=1)
        self.btn_move_up = tk.Button(self.listbox_frame, text=u"\u2191",
                                     command=self.move_up, font=("Arial", "14"), width=1)
        # Undo/Redoのボタン
        self.btn_undo = tk.Button(self.listbox_frame, text=u"\u21B6",
                                  command=self.undo)
        self.btn_redo = tk.Button(self.listbox_frame, text=u"\u21B7",
                                  command=self.redo)
        # ボタンの配置
        self.btn_frame.grid(row=1, column=0, pady=(0, 20))
        self.btn_add.grid(row=0, column=0, padx=10, sticky=tk.W + tk.E)
        self.btn_replace.grid(row=0, column=1, padx=10, sticky=tk.W + tk.E)

    # Entryの初期化
    def set_entry(self):
        # カンバス上の点の座標のテキストボックス
        # ラベル
        self.label_entry = tk.Label(self.entry_frame, text=messages["entry_label"])
        self.entry_x = tk.Entry(self.entry_frame, textvariable=self.var_entry_x, font=14, width=7)
        self.entry_y = tk.Entry(self.entry_frame, textvariable=self.var_entry_y, font=14, width=7)
        # テキストボックス・フレームの配置
        self.entry_frame.grid(row=0, column=0, pady=20)
        self.label_entry.grid(row=0, column=0, columnspan=2)
        self.entry_x.grid(row=1, column=0)
        self.entry_y.grid(row=1, column=1)

    # Listboxの初期化
    def set_list_box(self):
        # ラベル
        self.label_listbox = tk.Label(self.listbox_frame, text=messages["listbox_label"])
        # 点のリストボックス
        self.listbox_x = tk.Listbox(self.listbox_frame, font=14, height=20, width=7, exportselection=0)
        self.listbox_y = tk.Listbox(self.listbox_frame, font=14, height=20, width=7, exportselection=0)
        # Scrollbar
        # リストボックスのスクロールバー
        self.scrollbar_listbox = tk.Scrollbar(self.listbox_frame)
        self.listbox_x.config(yscrollcommand=self.scroll_listbox_x)
        self.listbox_y.config(yscrollcommand=self.scroll_listbox_y)
        self.scrollbar_listbox.config(command=self.scroll_scrollbar)
        # リストボックス・フレームの配置
        self.listbox_frame.grid(row=2, column=0, pady=(0, 20))
        self.label_listbox.grid(row=0, column=0, columnspan=4)
        self.btn_move_up.grid(row=1, column=0, sticky=tk.S)
        self.btn_delete.grid(row=2, column=0)
        self.btn_move_down.grid(row=3, column=0, sticky=tk.N)
        self.listbox_x.grid(row=1, column=1, rowspan=3, sticky=tk.W + tk.E + tk.N + tk.S)
        self.listbox_y.grid(row=1, column=2, rowspan=3, sticky=tk.W + tk.E + tk.N + tk.S)
        self.scrollbar_listbox.grid(row=1, column=3, rowspan=3, sticky=tk.W + tk.E + tk.N + tk.S)
        self.btn_undo.grid(row=4, column=1, columnspan=2, sticky=tk.W)
        self.btn_redo.grid(row=4, column=1, columnspan=2, sticky=tk.E)

    # メニューのラベルの設定
    def menu_arrangement(self):
        self.menubar.add_cascade(label=messages["file_menu"], menu=self.filemenu)
        self.menubar.add_cascade(label=messages["edit_menu"], menu=self.editmenu)
        self.menubar.add_cascade(label=messages["preview_menu"], menu=self.previewmenu)
        self.menubar.add_cascade(label=messages["background_menu"], menu=self.backgroundmenu)
        self.menubar.add_cascade(label=messages["options_menu"], menu=self.optionsmenu)
        self.menubar.add_cascade(label=messages["other_menu"], menu=self.othermenu)
