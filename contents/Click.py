#
# Click.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk


# クリック操作のクラス
class Click:

    # クリック・リストボックスX
    def select_listbox_x(self, *args):
        nx = self.listbox_x.curselection()
        ny = self.listbox_y.curselection()
        if ny != nx:
            self.listbox_y.selection_clear(0, tk.END)
            self.listbox_y.selection_set(nx)

        self.draw_everything()

    # クリック・リストボックスY
    def select_listbox_y(self, *args):
        nx = self.listbox_x.curselection()
        ny = self.listbox_y.curselection()
        if nx != ny:
            self.listbox_x.selection_clear(0, tk.END)
            self.listbox_x.selection_set(ny)

        self.draw_everything()

    # カンバス上でクリックした点の座標をテキストボックスに入力
    def click_canvas(self, event):
        x, y = self.get_point_from_event(event, transform=True)

        self.var_entry_x.set(x)
        self.var_entry_y.set(y)

        self.draw_everything()
        self.canvas.focus_set()

    # カンバス上でダブル・クリックした点をリストボックスで選定
    def double_click_canvas(self, event):
        assert self.listbox_x.size() == self.listbox_y.size()
        listbox_size = self.listbox_x.size()

        x, y = self.get_point_from_event(event, transform=False)

        for n in range(listbox_size):
            listbox_entry_x, listbox_entry_y = self.get_point_from_listbox(n)

            dist = (((listbox_entry_x - x) ** 2) + ((listbox_entry_y - y) ** 2)) ** 0.5
            if dist < 10:
                self.listbox_x.selection_clear(0, tk.END)
                self.listbox_x.selection_set(n)
                self.listbox_x.activate(n)
                self.listbox_x.see(n)

                self.listbox_y.selection_clear(0, tk.END)
                self.listbox_y.selection_set(n)

                self.double_click_selected()
                break

    # リストボックスでダブル・クリックした点をテキストボックスに入力
    def double_click_selected(self, *event):
        assert self.listbox_x.size() == self.listbox_y.size()
        assert self.listbox_x.curselection() == self.listbox_y.curselection()
        n = self.listbox_x.curselection()

        if n:
            x, y = self.get_point_from_listbox(n, transform=False)

            self.var_entry_x.set(x)
            self.var_entry_y.set(y)

            self.draw_everything()
            self.canvas.focus_set()
