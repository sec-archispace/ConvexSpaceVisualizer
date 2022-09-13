#
# Constants.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#
import json
from tkinter.messagebox import showwarning

# 定数類をまとめたファイル

# ファイル名の変数
# convexspaceheatmap
CONVEXSPACEHEATMAP_FOLDER = "convexspaceheatmap"
CONVEXSPACEHEATMAP_INPUT_FILE = CONVEXSPACEHEATMAP_FOLDER + "/polygons/input.csv"
CONVEXSPACEHEATMAP_OUTPUT_FILE = CONVEXSPACEHEATMAP_FOLDER + "/output.png"
CONVEXSPACEHEATMAP_EPROPERTIES_FILE = CONVEXSPACEHEATMAP_FOLDER + "/properties/enumeration.properties"
CONVEXSPACEHEATMAP_JAR_FILE = CONVEXSPACEHEATMAP_FOLDER + "/convexspaceheatmap.jar"

# polygons
INPUT_FOLDER = "polygons"

# properties
PROPERTIES_FOLDER = "properties"
MESSAGES_FILE = PROPERTIES_FOLDER + "/messages_jpn.json"

# メッセージ一覧を読み込む
try:
    json_file = open(f"{MESSAGES_FILE}", encoding="utf-8")
    messages = json.load(json_file)
except Exception as e:
    print(e)
    showwarning(title="Warning", message="'messages_eng.json' does not exist.\
                                          \nIt should be arranged in 'properties' folder.")

# メッセージの変数
CONFIRMATION_TITLE = messages["confirmation_title"]
CONFIRMATION_MESSAGE = messages["confirmation_message"]
OVERWRITE_MESSAGE = messages["overwrite_message"].format(CONVEXSPACEHEATMAP_INPUT_FILE, CONVEXSPACEHEATMAP_OUTPUT_FILE)
UNSAVED_CHANGES_MESSAGE = messages["unsaved_changes_message"]

# カーソル形の選択肢
OPTIONS_CURSOR_SHAPE = [
    messages["cursor_shape_dot"],
    messages["cursor_shape_circle"],
    messages["cursor_shape_circle_dot"],
    messages["cursor_shape_cross"]
]

# 位置の選択肢
OPTIONS_POS = [
    messages["pos_up_left"],
    messages["pos_down_left"],
    messages["pos_center"]
]

# 操作プレビューの選択肢
OPTIONS_PREVIEW = [
    messages["none"],
    messages["add"],
    messages["replace"],
    messages["delete"]
]
