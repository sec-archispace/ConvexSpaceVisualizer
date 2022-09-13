#
# Utils.py
#
# Copyright(c) 2021-2022 Systems Engineering Consultants Co.,LTD.
# All Rights Reserved.
# Systems Engineering Consultants Co.,LTD. Proprietary/Confidential.
#

# 共通関数

# 文字列が座標であるかの確認
def is_float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


# 座標を反転
def reverse_coord(coord, coord_max):
    if isinstance(coord, str):
        result = float(coord_max) - float(coord)
        if result == int(result):
            return str(int(result))
        return str(result)
    return coord_max - coord
