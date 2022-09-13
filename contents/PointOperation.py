#
# PointOperation.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk
from tkinter.messagebox import showwarning
from contents.Utils import is_float
from contents.Constants import messages


# 頂点の操作のクラス
class PointOperation:

    # テキストボックスの入力から点を取得
    def get_point_from_entry(self, transform=True):
        x = self.var_entry_x.get().strip()
        y = self.var_entry_y.get().strip()

        if is_float(x) and is_float(y):
            if transform:
                x, y = self.transform_to_pixel(x, y)

            return x, y

        return None, None

    # カンバスを選定
    def entry_return(self, *event):
        self.draw_everything()
        self.canvas.focus_set()

    # イベントから点を取得
    def get_point_from_event(self, event, transform=True):
        x, y = float(event.x), float(event.y)

        if transform:
            x, y = self.transform_to_coord(x, y)

        return x, y

    # 現在の座標を更新
    def update_current_coordinates(self, event):
        x, y = self.get_point_from_event(event, transform=True)

        self.canvas.itemconfigure(self.canvas.current_coordinates, text=f"{x:>10},{y:<10}")

    # テキストボックス入力座標をリストボックスに追加
    def add(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        n = self.listbox_x.curselection()

        x, y = self.get_point_from_entry(transform=False)
        if x is not None and y is not None:
            is_duplicated = self.check_vertex_duplication(x, y)
            if is_duplicated is True:
                return
            self.saved = False
            if n:
                self.listbox_x.insert(n, f"{x}")
                self.listbox_y.insert(n, f"{y}")

                self.listbox_x.selection_clear(0, tk.END)
                self.listbox_x.selection_set(n)
                self.listbox_x.activate(n)
                self.listbox_x.see(n)

                self.listbox_y.selection_clear(0, tk.END)
                self.listbox_y.selection_set(n)
            else:
                self.listbox_x.insert(tk.END, f"{x}")
                self.listbox_y.insert(tk.END, f"{y}")
                self.listbox_x.see(tk.END)

            self.add_to_history()

            self.draw_everything()
        else:
            error_message = ""
            if not is_float(x):
                if error_message:
                    error_message += "\n"
                error_message += messages["x_coord_error"]
            if not is_float(y):
                if error_message:
                    error_message += "\n"
                error_message += messages["y_coord_error"]
            showwarning(title=messages["warning_title"], message=error_message)

    # リストボックスで選定した点をテキストボックス入力座標と交換する
    def replace(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        n = self.listbox_x.curselection()

        x, y = self.get_point_from_entry(transform=False)
        if x is not None and y is not None:
            self.saved = False
            if n:
                self.listbox_x.delete(n)
                self.listbox_y.delete(n)
                self.listbox_x.insert(n, f"{x}")
                self.listbox_y.insert(n, f"{y}")

                self.listbox_x.selection_clear(0, tk.END)
                self.listbox_x.selection_set(n)
                self.listbox_x.activate(n)
                self.listbox_x.see(n)

                self.listbox_y.selection_clear(0, tk.END)
                self.listbox_y.selection_set(n)
            else:
                self.listbox_x.delete(tk.END)
                self.listbox_y.delete(tk.END)
                self.listbox_x.insert(tk.END, f"{x}")
                self.listbox_y.insert(tk.END, f"{y}")
                self.listbox_x.see(tk.END)

            self.add_to_history()

            self.draw_everything()
        else:
            error_message = ""
            if not is_float(x):
                if error_message:
                    error_message += "\n"
                error_message += messages["x_coord_error"]
            if not is_float(y):
                if error_message:
                    error_message += "\n"
                error_message += messages["y_coord_error"]
            showwarning(title=messages["warning_title"], message=error_message)

    # リストボックスで選定した点を削除
    def delete(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        listbox_size = self.listbox_x.size()
        n = self.listbox_x.curselection()

        if listbox_size == 0:
            return

        self.saved = False
        if n:
            self.listbox_x.delete(n)
            self.listbox_y.delete(n)

            self.listbox_x.selection_clear(0, tk.END)
            self.listbox_x.selection_set(n)
            self.listbox_x.activate(n)
            self.listbox_x.see(n)

            self.listbox_y.selection_clear(0, tk.END)
            self.listbox_y.selection_set(n)
        else:
            self.listbox_x.delete(tk.END)
            self.listbox_y.delete(tk.END)
            self.listbox_x.see(tk.END)

        self.add_to_history()

        self.draw_everything()

    # リストボックスで選定した点を一つ上の行の点と交換
    def move_up(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        n = self.listbox_x.curselection()

        if n and n[0] > 0:
            self.saved = False

            listbox_entry_x, listbox_entry_y = self.get_point_from_listbox(n, transform=False)
            self.listbox_x.delete(n)
            self.listbox_y.delete(n)
            self.listbox_x.insert(n[0] - 1, listbox_entry_x)
            self.listbox_y.insert(n[0] - 1, listbox_entry_y)

            self.listbox_x.selection_clear(0, tk.END)
            self.listbox_x.selection_set(n[0] - 1)
            self.listbox_x.activate(n[0] - 1)
            self.listbox_x.see(n[0] - 1)

            self.listbox_y.selection_clear(0, tk.END)
            self.listbox_y.selection_set(n[0] - 1)

            self.add_to_history()

            self.draw_everything()

    # リストボックスで選定した点を一つ下の行の点と交換
    def move_down(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        listbox_size = self.listbox_x.size()
        n = self.listbox_x.curselection()

        if n and n[0] < (listbox_size - 1):
            self.saved = False

            listbox_entry_x, listbox_entry_y = self.get_point_from_listbox(n, transform=False)
            self.listbox_x.delete(n)
            self.listbox_y.delete(n)
            self.listbox_x.insert(n[0] + 1, listbox_entry_x)
            self.listbox_y.insert(n[0] + 1, listbox_entry_y)

            self.listbox_x.selection_clear(0, tk.END)
            self.listbox_x.selection_set(n[0] + 1)
            self.listbox_x.activate(n[0] + 1)
            self.listbox_x.see(n[0] + 1)

            self.listbox_y.selection_clear(0, tk.END)
            self.listbox_y.selection_set(n[0] + 1)

            self.add_to_history()

            self.draw_everything()

    # 履歴に現状のリストボックスを追加
    def add_to_history(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()

        history_list_box = []
        for listbox_entry_x, listbox_entry_y in zip(self.listbox_x.get(0, tk.END), self.listbox_y.get(0, tk.END)):
            history_list_box.append(f"{listbox_entry_x},{listbox_entry_y}")

        self.history = self.history[self.history_pos:]
        self.history.insert(0, history_list_box)
        self.history_pos = 0

        if len(self.history) > 100:
            del self.history[-1]

    # Undo
    def undo(self, *event):
        if self.history_pos + 1 >= len(self.history):
            return

        self.history_pos += 1
        history_listbox = self.history[self.history_pos]

        self.listbox_x.delete(0, tk.END)
        self.listbox_y.delete(0, tk.END)

        for listbox_entry in history_listbox:
            x, y = listbox_entry.split(",")
            self.listbox_x.insert(tk.END, x)
            self.listbox_y.insert(tk.END, y)

        self.draw_everything()

    # Redo
    def redo(self, *event):
        if self.history_pos == 0:
            return

        self.history_pos -= 1
        history_listbox = self.history[self.history_pos]

        self.listbox_x.delete(0, tk.END)
        self.listbox_y.delete(0, tk.END)

        for listbox_entry in history_listbox:
            x, y = listbox_entry.split(",")
            self.listbox_x.insert(tk.END, x)
            self.listbox_y.insert(tk.END, y)

        self.draw_everything()

    # 点を上側に1pix移動させる
    def y_1up(self, event):
        x, y = self.get_point_from_entry()
        if x is None and y is None:
            return
        y -= 1
        self.update_coordinates(x, y)

    # 点を上側に10pix移動させる
    def y_10up(self, event):
        x, y = self.get_point_from_entry()
        if x is None and y is None:
            return
        y -= 10
        self.update_coordinates(x, y)

    # 点を下側に1pix移動させる
    def y_1down(self, event):
        x, y = self.get_point_from_entry()
        if x is None and y is None:
            return
        y += 1
        self.update_coordinates(x, y)

    # 点を下側に10pix移動させる
    def y_10down(self, event):
        x, y = self.get_point_from_entry()
        if x is None and y is None:
            return
        y += 10
        self.update_coordinates(x, y)

    # 点を右側に1pix移動させる
    def x_1right(self, event):
        x, y = self.get_point_from_entry()
        if x is None and y is None:
            return
        x += 1
        self.update_coordinates(x, y)

    # 点を右側に10pix移動させる
    def x_10right(self, event):
        x, y = self.get_point_from_entry()
        if x is None and y is None:
            return
        x += 10
        self.update_coordinates(x, y)

    # 点を左側に1pix移動させる
    def x_1left(self, event):
        x, y = self.get_point_from_entry()
        if x is None and y is None:
            return
        x -= 1
        self.update_coordinates(x, y)

    # 点を左側に10pix移動させる
    def x_10left(self, event):
        x, y = self.get_point_from_entry()
        if x is None and y is None:
            return
        x -= 10
        self.update_coordinates(x, y)

    # 点の移動操作に応じて、座標を更新する
    def update_coordinates(self, x, y):
        x = max(x, 0)
        x = min(x, self.canvas.canvas_width)
        y = max(y, 0)
        y = min(y, self.canvas.canvas_height)
        x, y = self.transform_to_coord(x, y)
        self.var_entry_x.set(x)
        self.var_entry_y.set(y)
        self.draw_everything()

    # 点の追加処理時、追加される点が既にある頂点と重複しているか調べる
    def check_vertex_duplication(self, x_new, y_new):
        listbox_size = self.listbox_x.size()
        for i in range(listbox_size):
            x, y = self.get_point_from_listbox(i, transform=False)
            if x == x_new and y == y_new:
                return True
        return False
