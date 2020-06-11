PLAY_MODE = 'tap'  # tap 无需root，sendevent需要root，区别见README

'''
如果使用adb shell sendevent （需要设备已经root）
则填写下列参数
'''
# 左上角坐标
LEFT_UP_X = 0xcd
LEFT_UP_Y = 0x67c
# 左下角坐标
LEFT_DOWN_X = 0x243
LEFT_DOWN_Y = 0x687
# 右上角坐标
RIGHT_UP_X = 0xc4
RIGHT_UP_Y = 0x384
# 右下角坐标
RIGHT_DOWN_X = 0x241
RIGHT_DOWN_Y = 0x37b
DEVICE = '/dev/input/event4'


'''
如果使用adb shell input tap （设备无需root）
则填写下列参数
'''
# for tap
# 左上角坐标
LEFT_UP_XX = 920
LEFT_UP_YY = 230
# 左下角坐标
LEFT_DOWN_XX = 920
LEFT_DOWN_YY = 580
# 右上角坐标
RIGHT_UP_XX = 1670
RIGHT_UP_YY = 230
# 右下角坐标
RIGHT_DOWN_XX = 1670
RIGHT_DOWN_YY = 580
####################
