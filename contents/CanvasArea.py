#
# CanvasArea.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import tkinter as tk
from decimal import Decimal, ROUND_HALF_UP
from PIL import Image, ImageOps, ImageTk
from tkinter import filedialog
from contents.CanvasAreaSettingWindow import CanvasAreaSettingWindow
from contents.Constants import messages, OPTIONS_POS, OPTIONS_CURSOR_SHAPE
canvas_options_popup = None  # キャンバスの設定ウィンドウが開いているかどうかの変数


# メインウィンドウのカンバス部分のクラス
class CanvasArea(tk.Frame):
    def __init__(self, master):
        self.master = master

        # 画像の変数
        self.image_background = Image
        self.image_background_zoomed = Image
        self.imagetk_background = ImageTk.PhotoImage

        # DoubleVar
        self.var_zoom = tk.DoubleVar(value=1.0)

        # IntVar
        # カンバス・グリッドの変数
        self.var_canvas_grid = tk.IntVar(value=100)
        self.var_canvas_show_axis_coord = tk.IntVar(value=1)
        self.var_canvas_show_cursor_coord = tk.IntVar(value=1)
        self.var_canvas_show_grid = tk.IntVar(value=1)
        # カンバス座標の変数
        self.var_canvas_x = tk.IntVar(value=800)
        self.var_canvas_y = tk.IntVar(value=600)
        # カンバス・サイズの変数
        self.var_canvas_x_pixel = tk.IntVar(value=800)
        self.var_canvas_y_pixel = tk.IntVar(value=600)
        # カーソル・サイズの変数
        self.var_cursor_size = tk.IntVar(value=10)
        # 画像反転の変数(bool)
        self.var_image_flip = tk.IntVar()
        # 画像表示の変数(bool)
        self.var_show_background = tk.IntVar()

        # StringVar
        # カーソル形の変数
        self.var_cursor_shape = tk.StringVar(value=OPTIONS_CURSOR_SHAPE[0])
        # 画像パスの変数
        self.var_image_background_path = tk.StringVar()
        # 画像位置の変数
        self.var_image_pos = tk.StringVar(value=OPTIONS_POS[0])

        # Canvas
        # カンバス初期化
        self.canvas = tk.Canvas(self.master.master, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=40, pady=40)
        self.calc_zoom()
        self.update_canvas()

    # 操作と処理のバインド
    def bind(self, action, func):
        self.canvas.bind(action, func)

    def create_line(self, x1, y1, x2, y2, fill="black", dash=(), width=1):
        self.canvas.create_line(x1, y1, x2, y2, fill=fill, dash=dash, width=width)

    # 消去
    def delete(self, s):
        self.canvas.delete(s)

    # ウィンドウのアクティベート
    def focus_set(self):
        self.canvas.focus_set()

    def itemconfigure(self, current_coordinates, text):
        self.canvas.itemconfigure(current_coordinates, text=text)

    # カンバス上の点の位置/座標の比率を計算
    def calc_zoom(self, *event):
        x = self.var_canvas_x.get()
        y = self.var_canvas_y.get()
        x_pixel = self.var_canvas_x_pixel.get()
        y_pixel = self.var_canvas_y_pixel.get()

        self.ratio = y / x

        if self.ratio >= y_pixel / x_pixel:
            self.var_zoom.set(float(y_pixel / y))
        else:
            self.var_zoom.set(float(x_pixel / x))

    # カンバスを更新
    def update_canvas(self, *event):
        self.canvas.config(width=self.var_canvas_x.get() * self.var_zoom.get() - 4,
                           height=self.var_canvas_y.get() * self.var_zoom.get() - 4)

        self.canvas.update()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

    # 画像をズーム
    def zoom_background_image(self, *event):
        x = float(self.image_background.size[0]) * self.var_zoom.get()
        y = float(self.image_background.size[1]) * self.var_zoom.get()
        self.image_background_zoomed = self.image_background.resize(
            (int(Decimal(x).to_integral_value(rounding=ROUND_HALF_UP)),
             int(Decimal(y).to_integral_value(rounding=ROUND_HALF_UP))),
            Image.ANTIALIAS)

    # カンバスをズーム
    def zoom_canvas(self, *event):
        x = self.var_canvas_x.get()
        y = self.var_canvas_y.get()
        x_pixel = self.var_canvas_x_pixel.get()
        y_pixel = self.var_canvas_y_pixel.get()

        if self.ratio >= y_pixel / x_pixel:
            y = y_pixel / self.var_zoom.get()
            x = y / self.ratio
        else:
            x = x_pixel / self.var_zoom.get()
            y = x * self.ratio

        self.var_canvas_x.set(int(Decimal(x).to_integral_value(rounding=ROUND_HALF_UP)))
        self.var_canvas_y.set(int(Decimal(y).to_integral_value(rounding=ROUND_HALF_UP)))

        self.update_canvas()

        if self.var_image_background_path.get():
            self.zoom_background_image()

    # 画像をファイルからロード
    def load_background_image_from_file(self, *event):
        self.image_background = Image.open(self.var_image_background_path.get())
        self.zoom_background_image()

    # 画像をファイルからロード
    def load_background_image(self, *event):
        file_name = filedialog.askopenfilename(initialdir="./")
        if file_name:
            self.var_image_background_path.set(file_name)
        else:
            return

        self.load_background_image_from_file()
        self.master.backgroundmenu.entryconfig(messages["show_image"], state="normal")
        self.var_show_background.set(1)

    # カンバスを設定
    def config_canvas(self, *event):
        global canvas_options_popup
        if canvas_options_popup is None or not canvas_options_popup.winfo_exists():
            canvas_options_popup = CanvasAreaSettingWindow(self.master)
            canvas_options_popup.lift()
            canvas_options_popup.focus_force()
            canvas_options_popup.wait_window()

        self.calc_zoom()
        self.update_canvas()

        if self.var_image_background_path.get():
            self.zoom_background_image()

    # 画像をカンバス上で表示
    def draw_background_image(self, *event):
        if self.var_image_flip.get():
            self.imagetk_background = ImageTk.PhotoImage(ImageOps.flip(self.image_background_zoomed))
        else:
            self.imagetk_background = ImageTk.PhotoImage(self.image_background_zoomed)

        image_pos = self.var_image_pos.get()
        if image_pos == messages["pos_center"]:
            self.canvas.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.imagetk_background)
        elif image_pos == messages["pos_up_left"]:
            self.canvas.create_image(0, 0, anchor="nw", image=self.imagetk_background)
        elif image_pos == messages["pos_down_left"]:
            self.canvas.create_image(0, self.canvas_height, anchor="sw", image=self.imagetk_background)

    # 画像を表示/未表示
    def change_show_background_image(self, *event):
        if not self.var_image_background_path.get():
            return

        self.var_show_background.set(1 - self.var_show_background.get())

    # グリッドをカンバス上で表示
    def draw_grid(self, *event):
        canvas_grid = self.var_canvas_grid.get()
        canvas_x = self.var_canvas_x.get()
        canvas_y = self.var_canvas_y.get()

        for i in range(0, canvas_x, canvas_grid):
            pixel = i * self.var_zoom.get()
            if self.var_canvas_show_grid.get():
                self.canvas.create_line([(pixel, 0), (pixel, self.canvas_height)], dash=(4, 1))
            if i != 0 and self.var_canvas_show_axis_coord.get():
                if self.master.var_reverse_y.get():
                    offset = self.canvas_height - 15
                else:
                    offset = 10
                self.canvas.create_text(pixel, offset, text=f"{i}")

        for i in range(0, canvas_y, canvas_grid):
            if self.master.var_reverse_y.get():
                pixel = self.canvas_height - i * self.var_zoom.get()
            else:
                pixel = i * self.var_zoom.get()
            if self.var_canvas_show_grid.get():
                self.canvas.create_line([(0, pixel), (self.canvas_width, pixel)], dash=(4, 1))
            if i != 0 and self.var_canvas_show_axis_coord.get():
                offset = 7 + 3 * len(str(i))
                self.canvas.create_text(offset, pixel, text=f"{i}")

    # 原点の座標を表示
    def draw_current_coordinates(self, x, y):
        if x is not None and y is not None:
            self.current_coordinates = self.canvas.create_text(self.canvas_width,
                                                               8, text=f"{x:>10},{y:<10}", anchor="ne")
        else:
            self.current_coordinates = self.canvas.create_text(self.canvas_width, 8, text="", anchor="ne")

    # カンバス上で点を表示
    def draw_point(self, x, y, color="#ff0000"):
        radius = int(self.var_cursor_size.get() / 2)
        if radius == 0:
            self.canvas.create_line(x, y, x + 1, y, fill=color)
        else:
            cursor_shape = self.var_cursor_shape.get()
            if cursor_shape == messages["cursor_shape_dot"]:
                self.canvas.create_oval((x - radius), (y - radius), (x + radius), (y + radius),
                                        fill=color, outline="")
            elif cursor_shape == messages["cursor_shape_circle"]:
                self.canvas.create_oval((x - radius), (y - radius), (x + radius), (y + radius),
                                        fill="", outline=color)
            elif cursor_shape == messages["cursor_shape_circle_dot"]:
                self.canvas.create_oval((x - radius), (y - radius), (x + radius), (y + radius),
                                        fill="", outline=color)
                self.canvas.create_line(x, y, x + 1, y, fill=color)
            elif cursor_shape == messages["cursor_shape_cross"]:
                self.canvas.create_line((x - radius), (y - radius), (x + radius + 1), (y + radius + 1),
                                        fill=color)
                self.canvas.create_line((x - radius), (y + radius), (x + radius + 1), (y - radius - 1),
                                        fill=color)
