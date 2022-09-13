#
# ListBoxOperation.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk
from decimal import Decimal, ROUND_HALF_UP
from tkinter.messagebox import askyesno
from contents.Utils import reverse_coord
from contents.Constants import messages, CONFIRMATION_TITLE, CONFIRMATION_MESSAGE, UNSAVED_CHANGES_MESSAGE


# リストボックスの操作のクラス
class ListBoxOperation:

    # スクロール・リストボックスX
    def scroll_listbox_x(self, *args):
        if self.listbox_y.yview() != self.listbox_x.yview():
            self.listbox_y.yview_moveto(args[0])
        self.scrollbar_listbox.set(*args)

    # スクロール・リストボックスY
    def scroll_listbox_y(self, *args):
        if self.listbox_x.yview() != self.listbox_y.yview():
            self.listbox_x.yview_moveto(args[0])
        self.scrollbar_listbox.set(*args)

    # スクロール・スクロールバー
    def scroll_scrollbar(self, *args):
        self.listbox_x.yview(*args)
        self.listbox_y.yview(*args)

    # ピクセル値に変換
    def transform_to_pixel(self, x=0, y=0):
        if self.var_reverse_y.get():
            y = reverse_coord(y, self.canvas.var_canvas_y.get())

        x = float(x) * self.canvas.var_zoom.get()
        y = float(y) * self.canvas.var_zoom.get()
        x = int(Decimal(x).to_integral_value(rounding=ROUND_HALF_UP))
        y = int(Decimal(y).to_integral_value(rounding=ROUND_HALF_UP))

        return x, y

    # 座標値に変換
    def transform_to_coord(self, x=0, y=0):
        if self.var_reverse_y.get():
            y = reverse_coord(y, self.canvas.canvas_height)

        x = round(x / self.canvas.var_zoom.get(), self.var_round.get())
        y = round(y / self.canvas.var_zoom.get(), self.var_round.get())

        if x == int(x):
            x = int(x)
        if y == int(y):
            y = int(y)

        return str(x), str(y)

    # リストボックスでの選定をクリア
    def clear_selection(self, *event):
        if isinstance(event[0].widget, tk.Tk):
            self.listbox_x.selection_clear(0, tk.END)
            self.listbox_y.selection_clear(0, tk.END)
            self.master.focus_set()
            self.draw_everything()

    # テキストボックスとリストボックスをクリア
    def clear_all(self, *event):
        if not self.saved:
            answer = askyesno(title=CONFIRMATION_TITLE,
                              message=UNSAVED_CHANGES_MESSAGE + "\n" + CONFIRMATION_MESSAGE)
            if not answer:
                return

        self.var_poly_path.set("")

        self.var_entry_x.set("")
        self.var_entry_y.set("")

        while self.listbox_x.size() > 0:
            self.listbox_x.delete(tk.END)
        while self.listbox_y.size() > 0:
            self.listbox_y.delete(tk.END)

        self.canvas.var_show_background.set(0)
        self.backgroundmenu.entryconfig(messages["show_image"], state="disabled")

        self.saved = True
        self.clear_history()

        self.draw_everything()

    # リストボックスで選択した点の取得
    def get_point_from_listbox(self, n, transform=True):
        x, y = self.listbox_x.get(n), self.listbox_y.get(n)

        if transform:
            x, y = self.transform_to_pixel(x, y)

        return x, y

    # 履歴をクリア
    def clear_history(self, *event):
        self.history = []
        self.history_pos = 0
        self.add_to_history()
