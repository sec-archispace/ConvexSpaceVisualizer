#
# CommandBind.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk
from contents.Constants import messages, OPTIONS_POS, OPTIONS_PREVIEW, OPTIONS_CURSOR_SHAPE


# メインウィンドウのコマンドのバインドを行うクラス
class CommandBind:
    # キーへのコマンドの割り当て
    def key_command_bind(self):
        # コマンドのバインド
        self.master.bind('<Button 1>', self.clear_selection)
        self.master.bind('<Control-n>', self.clear_all)
        self.master.bind('<Control-o>', self.load)
        self.master.bind('<Control-s>', self.save)
        self.master.bind('<Control-Shift-S>', self.save_as)
        self.master.bind('<Control-q>', self.quit)
        self.master.bind('<Control-Shift-N>', lambda event: self.var_preview.set(OPTIONS_PREVIEW[0]))
        self.master.bind('<Control-Shift-A>', lambda event: self.var_preview.set(OPTIONS_PREVIEW[1]))
        self.master.bind('<Control-Shift-R>', lambda event: self.var_preview.set(OPTIONS_PREVIEW[2]))
        self.master.bind('<Control-Shift-D>', lambda event: self.var_preview.set(OPTIONS_PREVIEW[3]))
        self.master.bind('<Control-l>', self.load_background_image)
        self.master.bind('<Control-b>', self.change_show_background_image)
        self.master.bind('<Control-z>', self.undo)
        self.master.bind('<Control-y>', self.redo)
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        self.canvas.bind('<Motion>', self.update_current_coordinates)
        self.canvas.bind('<Button 1>', self.click_canvas)
        self.canvas.bind('<Double-1>', self.double_click_canvas)
        # カーソルキー
        self.canvas.bind('<Up>', self.y_1up)
        self.canvas.bind('<Down>', self.y_1down)
        self.canvas.bind('<Left>', self.x_1left)
        self.canvas.bind('<Right>', self.x_1right)
        self.canvas.bind('<Control-Up>', self.y_10up)
        self.canvas.bind('<Control-Down>', self.y_10down)
        self.canvas.bind('<Control-Left>', self.x_10left)
        self.canvas.bind('<Control-Right>', self.x_10right)

        self.canvas.bind('<Control-a>', self.add)
        self.canvas.bind('<Control-r>', self.replace)
        self.canvas.bind('<Control-d>', self.delete)
        self.canvas.bind('<Control-Shift-Up>', self.move_up)
        self.canvas.bind('<Control-Shift-Down>', self.move_down)
        self.canvas.bind('<space>', self.add)
        self.canvas.bind('<Return>', self.replace)

        self.entry_x.bind('<FocusOut>', self.draw_everything)
        self.entry_x.bind('<Return>', self.entry_return)
        self.entry_y.bind('<FocusOut>', self.draw_everything)
        self.entry_y.bind('<Return>', self.entry_return)

        self.listbox_x.bind('<<ListboxSelect>>', self.select_listbox_x)
        self.listbox_x.bind('<Double-1>', self.double_click_selected)
        self.listbox_x.bind('<Control-a>', self.add)
        self.listbox_x.bind('<Control-r>', self.replace)
        self.listbox_x.bind('<Control-d>', self.delete)
        self.listbox_x.bind('<Control-Shift-Up>', self.move_up)
        self.listbox_x.bind('<Control-Shift-Down>', self.move_down)
        self.listbox_y.bind('<<ListboxSelect>>', self.select_listbox_y)
        self.listbox_y.bind('<Double-1>', self.double_click_selected)
        self.listbox_y.bind('<Control-a>', self.add)
        self.listbox_y.bind('<Control-r>', self.replace)
        self.listbox_y.bind('<Control-d>', self.delete)
        self.listbox_y.bind('<Control-Shift-Up>', self.move_up)
        self.listbox_y.bind('<Control-Shift-Down>', self.move_down)

        self.canvas.var_cursor_shape.trace("w", self.draw_everything)
        self.canvas.var_cursor_size.trace("w", self.draw_everything)
        self.canvas.var_image_pos.trace("w", self.draw_everything)
        self.canvas.var_zoom.trace("w", self.zoom_canvas)

        self.var_origin.trace("w", self.change_origin)
        self.var_preview.trace("w", self.draw_everything)

    # メニュー・ショートカットへのコマンドの割り当て
    def menu_command_bind(self):
        self.file_menu_bind()
        self.edit_menu_bind()
        self.preview_menu_bind()
        self.background_menu_bind()
        self.options_menu_bind()
        self.other_menu_bind()

    # Fileメニューのバインド
    def file_menu_bind(self):
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=messages["file_new"], command=self.clear_all, accelerator="Ctrl+N")
        self.filemenu.add_command(label=messages["file_open"], command=self.load, accelerator="Ctrl+O")
        self.filemenu.add_separator()
        self.filemenu.add_command(label=messages["file_save"], command=self.save, accelerator="Ctrl+S")
        self.filemenu.add_command(label=messages["file_save_as"], command=self.save_as, accelerator="Ctrl+Shift+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label=messages["file_exit"], command=self.quit, accelerator="Ctrl+Q")

    # Editメニューのバインド
    def edit_menu_bind(self):
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label=messages["undo"], command=self.undo, accelerator="Ctrl+Z")
        self.editmenu.add_command(label=messages["redo"], command=self.redo, accelerator="Ctrl+Y")
        self.editmenu.add_separator()
        self.editmenu.add_command(label=messages["add"], command=self.add, accelerator="Ctrl+A")
        self.editmenu.add_command(label=messages["replace"], command=self.replace, accelerator="Ctrl+R")
        self.editmenu.add_command(label=messages["delete"], command=self.delete, accelerator="Ctrl+D")
        self.editmenu.add_separator()
        self.editmenu.add_command(label=messages["move_up"], command=self.move_up, accelerator="Ctrl+Shift+Up")
        self.editmenu.add_command(label=messages["move_down"], command=self.move_down, accelerator="Ctrl+Shift+Down")

    # Previewメニューのバインド
    def preview_menu_bind(self):
        self.previewmenu = tk.Menu(self.menubar, tearoff=0)
        self.previewmenu.add_radiobutton(label=OPTIONS_PREVIEW[0], variable=self.var_preview,
                                         value=OPTIONS_PREVIEW[0], accelerator="Ctrl+Shift+N")
        self.previewmenu.add_radiobutton(label=OPTIONS_PREVIEW[1], variable=self.var_preview,
                                         value=OPTIONS_PREVIEW[1], accelerator="Ctrl+Shift+A")
        self.previewmenu.add_radiobutton(label=OPTIONS_PREVIEW[2], variable=self.var_preview,
                                         value=OPTIONS_PREVIEW[2], accelerator="Ctrl+Shift+R")
        self.previewmenu.add_radiobutton(label=OPTIONS_PREVIEW[3], variable=self.var_preview,
                                         value=OPTIONS_PREVIEW[3], accelerator="Ctrl+Shift+D")

    # Backgroundメニューのバインド
    def background_menu_bind(self):
        self.backgroundmenu = tk.Menu(self.menubar, tearoff=0)
        self.backgroundmenu.add_command(label=messages["load_image"],
                                        command=self.load_background_image, accelerator="Ctrl+L")
        self.backgroundmenu.add_checkbutton(label=messages["show_image"], onvalue=1, offvalue=0,
                                            variable=self.canvas.var_show_background,
                                            command=self.draw_everything, accelerator="Ctrl+B", state="disabled")
        self.backgroundmenu.add_separator()
        self.backgroundmenu.add_checkbutton(label=messages["flip_image"], onvalue=1, offvalue=0,
                                            variable=self.canvas.var_image_flip,
                                            command=self.draw_everything)
        self.backgroundposmenu = tk.Menu(self.backgroundmenu, tearoff=0)
        self.backgroundposmenu.add_radiobutton(label=OPTIONS_POS[0], variable=self.canvas.var_image_pos,
                                               value=OPTIONS_POS[0])
        self.backgroundposmenu.add_radiobutton(label=OPTIONS_POS[1], variable=self.canvas.var_image_pos,
                                               value=OPTIONS_POS[1])
        self.backgroundposmenu.add_radiobutton(label=OPTIONS_POS[2], variable=self.canvas.var_image_pos,
                                               value=OPTIONS_POS[2])
        self.backgroundmenu.add_cascade(label=messages["pos_image"], menu=self.backgroundposmenu)
        self.backgroundmenu.add_separator()
        self.backgroundmenu.add_command(label=messages["config_image"], command=self.config_image)
        self.backgroundmenu.add_command(label=messages["gen_image"], command=self.generate_background_image)

    # Optionsメニューのバインド
    def options_menu_bind(self):
        self.optionsmenu = tk.Menu(self.menubar, tearoff=0)
        self.optionsmenu.add_command(label=messages["config_canvas"], command=self.config_canvas)
        self.optionszoommenu = tk.Menu(self.optionsmenu, tearoff=0)
        self.optionszoommenu.add_radiobutton(label="10%", variable=self.canvas.var_zoom, value=0.1)
        self.optionszoommenu.add_radiobutton(label="25%", variable=self.canvas.var_zoom, value=0.25)
        self.optionszoommenu.add_radiobutton(label="50%", variable=self.canvas.var_zoom, value=0.5)
        self.optionszoommenu.add_radiobutton(label="75%", variable=self.canvas.var_zoom, value=0.75)
        self.optionszoommenu.add_radiobutton(label="100%", variable=self.canvas.var_zoom, value=1.0)
        self.optionszoommenu.add_radiobutton(label="125%", variable=self.canvas.var_zoom, value=1.25)
        self.optionszoommenu.add_radiobutton(label="150%", variable=self.canvas.var_zoom, value=1.5)
        self.optionszoommenu.add_radiobutton(label="175%", variable=self.canvas.var_zoom, value=1.75)
        self.optionszoommenu.add_radiobutton(label="200%", variable=self.canvas.var_zoom, value=2.0)
        self.optionszoommenu.add_radiobutton(label="250%", variable=self.canvas.var_zoom, value=2.5)
        self.optionszoommenu.add_radiobutton(label="300%", variable=self.canvas.var_zoom, value=3.0)
        self.optionszoommenu.add_radiobutton(label="400%", variable=self.canvas.var_zoom, value=4.0)
        self.optionszoommenu.add_radiobutton(label="500%", variable=self.canvas.var_zoom, value=5.0)
        self.optionszoommenu.add_radiobutton(label="600%", variable=self.canvas.var_zoom, value=6.0)
        self.optionszoommenu.add_radiobutton(label="800%", variable=self.canvas.var_zoom, value=8.0)
        self.optionszoommenu.add_radiobutton(label="1000%", variable=self.canvas.var_zoom, value=10.0)
        self.optionsmenu.add_cascade(label=messages["zoom"], menu=self.optionszoommenu)
        self.optionsmenu.add_separator()
        self.optionsmenu.add_checkbutton(label=messages["canvas_show_grid"], onvalue=1, offvalue=0,
                                         variable=self.canvas.var_canvas_show_grid, command=self.draw_everything)
        self.optionsmenu.add_checkbutton(label=messages["canvas_show_axis_coord"], onvalue=1, offvalue=0,
                                         variable=self.canvas.var_canvas_show_axis_coord, command=self.draw_everything)
        self.optionsmenu.add_checkbutton(label=messages["canvas_show_cursor_coord"], onvalue=1, offvalue=0,
                                         variable=self.canvas.var_canvas_show_cursor_coord,
                                         command=self.draw_everything)
        self.optionsmenu.add_separator()
        self.optionscursorshapemenu = tk.Menu(self.optionsmenu, tearoff=0)
        self.optionscursorshapemenu.add_radiobutton(label=OPTIONS_CURSOR_SHAPE[0],
                                                    variable=self.canvas.var_cursor_shape,
                                                    value=OPTIONS_CURSOR_SHAPE[0])
        self.optionscursorshapemenu.add_radiobutton(label=OPTIONS_CURSOR_SHAPE[1],
                                                    variable=self.canvas.var_cursor_shape,
                                                    value=OPTIONS_CURSOR_SHAPE[1])
        self.optionscursorshapemenu.add_radiobutton(label=OPTIONS_CURSOR_SHAPE[2],
                                                    variable=self.canvas.var_cursor_shape,
                                                    value=OPTIONS_CURSOR_SHAPE[2])
        self.optionscursorshapemenu.add_radiobutton(label=OPTIONS_CURSOR_SHAPE[3],
                                                    variable=self.canvas.var_cursor_shape,
                                                    value=OPTIONS_CURSOR_SHAPE[3])
        self.optionsmenu.add_cascade(label=messages["cursor_shape"], menu=self.optionscursorshapemenu)
        self.optionscursorsizemenu = tk.Menu(self.optionsmenu, tearoff=0)
        self.optionscursorsizemenu.add_radiobutton(label="1", variable=self.canvas.var_cursor_size, value=1)
        self.optionscursorsizemenu.add_radiobutton(label="2", variable=self.canvas.var_cursor_size, value=2)
        self.optionscursorsizemenu.add_radiobutton(label="5", variable=self.canvas.var_cursor_size, value=5)
        self.optionscursorsizemenu.add_radiobutton(label="7", variable=self.canvas.var_cursor_size, value=7)
        self.optionscursorsizemenu.add_radiobutton(label="10", variable=self.canvas.var_cursor_size, value=10)
        self.optionsmenu.add_cascade(label=messages["cursor_size"], menu=self.optionscursorsizemenu)

    # Otherメニューのバインド
    def other_menu_bind(self):
        self.othermenu = tk.Menu(self.menubar, tearoff=0)
        self.othermenu.add_checkbutton(label=messages["loop"], onvalue=1, offvalue=0,
                                       variable=self.var_loop, command=self.draw_everything)
        self.otheroriginmenu = tk.Menu(self.othermenu, tearoff=0)
        self.otheroriginmenu.add_radiobutton(label=OPTIONS_POS[0], variable=self.var_origin, value=OPTIONS_POS[0])
        self.otheroriginmenu.add_radiobutton(label=OPTIONS_POS[1], variable=self.var_origin, value=OPTIONS_POS[1])
        self.othermenu.add_cascade(label=messages["origin"], menu=self.otheroriginmenu)
