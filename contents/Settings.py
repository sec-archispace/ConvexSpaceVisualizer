#
# Settings.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
from contents.HeatMapConfigWindow import HeatMapConfigWindow
from contents.Constants import messages
heatmap_options_popup = None  # ヒートマップの生成に関する設定ウィンドウが開いているかどうかの変数


# 設定関連の処理のクラス
class Settings:

    # カンバスを設定
    def config_canvas(self, *event):
        self.canvas.config_canvas()

        self.draw_everything()

    # カンバスをズーム
    def zoom_canvas(self, *event):
        self.canvas.zoom_canvas()

        self.draw_everything()

    # 座標原点を変更
    def change_origin(self, *event):
        if ((self.var_origin.get() == messages["pos_up_left"] and not self.var_reverse_y.get()) or
                (self.var_origin.get() == messages["pos_down_left"] and self.var_reverse_y.get())):
            return

        if self.var_reverse_y.get():
            self.var_reverse_y.set(0)
        else:
            self.var_reverse_y.set(1)

        self.reverse_y()

    # 画像を設定
    def config_image(self, *event):
        global heatmap_options_popup
        if heatmap_options_popup is None or not heatmap_options_popup.winfo_exists():
            heatmap_options_popup = HeatMapConfigWindow(self)
            heatmap_options_popup.lift()
            heatmap_options_popup.focus_force()
            heatmap_options_popup.wait_window()

    # 画像を表示/未表示
    def change_show_background_image(self, *event):
        self.canvas.change_show_background_image()

        self.draw_everything()
