#
# DrawingProcessing.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk
from contents.Utils import is_float, reverse_coord
from contents.Constants import messages


# カンバス部分の描画処理のクラス
class DrawingProcessing:
    # リストボックスでの多角形をカンバス上で表示(プレビューを含め)
    def draw_listbox(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        listbox_size = self.listbox_x.size()
        n = self.listbox_x.curselection()

        option_menu = self.var_preview.get()

        if option_menu != messages["none"]:
            entry_x, entry_y = self.get_point_from_entry()

            if entry_x is not None and entry_y is not None:
                if n:
                    n = n[0]
                else:
                    n = listbox_size - 1
                    if option_menu == messages["add"]:
                        n += 1

                preview_n = (n, n + 1)
            else:
                preview_n = ()
        else:
            preview_n = ()

        prev_x = None
        prev_y = None
        for i in range(listbox_size):
            next_x, next_y = self.get_point_from_listbox(i)

            if prev_x is not None and prev_y is not None and i not in preview_n:
                self.canvas.create_line(prev_x, prev_y, next_x, next_y, width=1.5)

            prev_x, prev_y = next_x, next_y

        if self.var_loop.get() and listbox_size > 2\
           and listbox_size not in preview_n and 0 not in preview_n:
            prev_x, prev_y = self.get_point_from_listbox(tk.END)
            next_x, next_y = self.get_point_from_listbox(0)

            self.canvas.create_line(prev_x, prev_y, next_x, next_y, width=1.5)

        if preview_n and listbox_size > 0:
            if n == 0:
                prev_x, prev_y = self.get_point_from_listbox(tk.END)
                curr_x, curr_y = self.get_point_from_listbox(n)
                if listbox_size > 1:
                    next_x, next_y = self.get_point_from_listbox(n + 1)
                else:
                    next_x, next_y = curr_x, curr_y
            elif n == listbox_size - 1:
                prev_x, prev_y = self.get_point_from_listbox(n - 1)
                curr_x, curr_y = self.get_point_from_listbox(n)
                next_x, next_y = self.get_point_from_listbox(0)
            elif n == listbox_size:
                prev_x, prev_y = self.get_point_from_listbox(tk.END)
                curr_x, curr_y = self.get_point_from_listbox(0)
                next_x, next_y = curr_x, curr_y
            else:
                prev_x, prev_y = self.get_point_from_listbox(n - 1)
                curr_x, curr_y = self.get_point_from_listbox(n)
                if listbox_size > 1:
                    next_x, next_y = self.get_point_from_listbox(n + 1)
                else:
                    next_x, next_y = curr_x, curr_y

            if option_menu == messages["add"]:
                self.draw_preview_add_operation(n, listbox_size, entry_x, entry_y,
                                                curr_x, curr_y, prev_x, prev_y,
                                                next_x, next_y)

            elif option_menu == messages["replace"]:
                self.draw_preview_replace_operation(n, listbox_size, entry_x, entry_y,
                                                    curr_x, curr_y, prev_x, prev_y,
                                                    next_x, next_y)

            elif option_menu == messages["delete"]:
                self.draw_preview_delete_operation(n, listbox_size, curr_x, curr_y,
                                                   prev_x, prev_y, next_x, next_y)

    # リストボックスで選定した点をカンバス上で表示
    def draw_listbox_selected(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        listbox_size = self.listbox_x.size()
        n = self.listbox_x.curselection()

        if n:
            x, y = self.get_point_from_listbox(n)
            self.canvas.draw_point(x, y, color="#0000ff")
        elif listbox_size == 1:
            x, y = self.get_point_from_listbox(0)
            self.canvas.draw_point(x, y, color="#000000")

    # テキストボックス入力座標をカンバス上で表示
    def draw_entry(self, *event):
        x, y = self.get_point_from_entry()

        if x is not None and y is not None:
            self.canvas.draw_point(x, y)

    # 原点の座標を表示
    def draw_current_coordinates(self, *event):
        x, y = self.get_point_from_entry(transform=False)

        self.canvas.draw_current_coordinates(x, y)

    # カンバス上でリストボックス・テキストボックス入力座標・選定した点を表示
    def draw_everything(self, *event):
        self.canvas.delete("all")

        if self.canvas.var_show_background.get():
            self.canvas.draw_background_image()

        if self.canvas.var_canvas_grid.get():
            self.canvas.draw_grid()

        self.draw_listbox()

        self.draw_entry()

        self.draw_listbox_selected()

        if self.canvas.var_canvas_show_cursor_coord.get():
            self.draw_current_coordinates()

    # 全て点のy座標を反転
    def reverse_y(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        listbox_size = self.listbox_x.size()
        n = self.listbox_x.curselection()

        if listbox_size > 0:
            self.saved = False

        reverse_list_box = []
        for listbox_entry_x, listbox_entry_y in zip(self.listbox_x.get(0, tk.END), self.listbox_y.get(0, tk.END)):
            x, y = listbox_entry_x, listbox_entry_y
            y = reverse_coord(y, self.canvas.var_canvas_y.get())
            reverse_list_box.append(f"{x},{y}")

        self.listbox_x.delete(0, tk.END)
        self.listbox_y.delete(0, tk.END)

        for listbox_entry in reverse_list_box:
            x, y = listbox_entry.split(",")
            self.listbox_x.insert(tk.END, x)
            self.listbox_y.insert(tk.END, y)

        if n:
            self.listbox_x.selection_set(n[0])
            self.listbox_x.activate(n[0])
            self.listbox_x.see(n[0])

            self.listbox_y.selection_set(n[0])

        y = self.var_entry_y.get().strip()
        if is_float(y):
            y = reverse_coord(y, self.canvas.var_canvas_y.get())
            self.var_entry_y.set(y)

        for listbox in self.history:
            for i, listbox_entry in enumerate(listbox):
                x, y = listbox_entry.split(",")
                y = reverse_coord(y, self.canvas.var_canvas_y.get())
                listbox[i] = f"{x},{y}"

        self.draw_everything()

    # 点の追加操作のpreviewを描画
    def draw_preview_add_operation(self, n, listbox_size, entry_x, entry_y,
                                   curr_x, curr_y, prev_x, prev_y, next_x,
                                   next_y):
        if n == 0:
            self.canvas.create_line(entry_x, entry_y, curr_x, curr_y,
                                    width=1.5, dash=(1, 1))
            if self.var_loop.get() and listbox_size > 1:
                self.canvas.create_line(prev_x, prev_y, entry_x, entry_y,
                                        width=1.5, dash=(1, 1))
                self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                        width=1, fill="grey")
            self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                    width=1.5)
        elif n == listbox_size - 1:
            self.canvas.create_line(prev_x, prev_y, entry_x, entry_y,
                                    width=1.5, dash=(1, 1))
            self.canvas.create_line(entry_x, entry_y, curr_x, curr_y,
                                    width=1.5, dash=(1, 1))
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                    width=1, fill="grey")
            if self.var_loop.get() and listbox_size > 1:
                self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                        width=1.5)
        elif n == listbox_size:
            self.canvas.create_line(prev_x, prev_y, entry_x, entry_y,
                                    width=1.5, dash=(1, 1))
            if self.var_loop.get() and listbox_size > 1:
                self.canvas.create_line(entry_x, entry_y, curr_x, curr_y,
                                        width=1.5, dash=(1, 1))
                if listbox_size > 2:
                    self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                            width=1, fill="grey")
        else:
            self.canvas.create_line(prev_x, prev_y, entry_x, entry_y,
                                    width=1.5, dash=(1, 1))
            self.canvas.create_line(entry_x, entry_y, curr_x, curr_y,
                                    width=1.5, dash=(1, 1))
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                    width=1, fill="grey")
            self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                    width=1.5)

    # 点の交換操作のpreviewを描画
    def draw_preview_replace_operation(self, n, listbox_size, entry_x, entry_y,
                                       curr_x, curr_y, prev_x, prev_y, next_x,
                                       next_y):
        if n == 0:
            self.canvas.create_line(entry_x, entry_y, next_x, next_y,
                                    width=1.5, dash=(1, 1))
            self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                    width=1, fill="grey")
            if self.var_loop.get() and listbox_size > 2:
                self.canvas.create_line(prev_x, prev_y, entry_x, entry_y,
                                        width=1.5, dash=(1, 1))
                self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                        width=1, fill="grey")
        elif n == listbox_size - 1:
            self.canvas.create_line(prev_x, prev_y, entry_x, entry_y,
                                    width=1.5, dash=(1, 1))
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                    width=1, fill="grey")
            if self.var_loop.get() and listbox_size > 2:
                self.canvas.create_line(entry_x, entry_y, next_x, next_y,
                                        width=1.5, dash=(1, 1))
                self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                        width=1, fill="grey")
        else:
            self.canvas.create_line(prev_x, prev_y, entry_x, entry_y,
                                    width=1.5, dash=(1, 1))
            self.canvas.create_line(entry_x, entry_y, next_x, next_y,
                                    width=1.5, dash=(1, 1))
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                    width=1, fill="grey")
            self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                    width=1, fill="grey")

    # 点の削除操作のpreviewを描画
    def draw_preview_delete_operation(self, n, listbox_size, curr_x, curr_y,
                                      prev_x, prev_y, next_x, next_y):
        if n == 0:
            self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                    width=1, fill="grey")
            if self.var_loop.get() and listbox_size > 2:
                self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                        width=1, fill="grey")
                if listbox_size > 3:
                    self.canvas.create_line(prev_x, prev_y, next_x, next_y,
                                            width=1.5, dash=(1, 1))
        elif n == listbox_size - 1:
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                    width=1, fill="grey")
            if self.var_loop.get() and listbox_size > 2:
                self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                        width=1, fill="grey")
                if listbox_size > 3:
                    self.canvas.create_line(prev_x, prev_y, next_x, next_y,
                                            width=1.5, dash=(1, 1))
        else:
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y,
                                    width=1, fill="grey")
            self.canvas.create_line(curr_x, curr_y, next_x, next_y,
                                    width=1, fill="grey")
            self.canvas.create_line(prev_x, prev_y, next_x, next_y,
                                    width=1.5, dash=(1, 1))
