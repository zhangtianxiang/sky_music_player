# by ztx97
# https://github.com/zhangtianxiang
import os
import sys
import pprint
import time
from config import *


########## 参数 ##########
DEFAULT_CLICK_SPACE = 0.5
PANEL_ROWS = 3
PANEL_COLUMNS = 5

EV_ABS = 0x0003
ABS_MT_PRESSURE = 0x003a  # 压力
ABS_MT_PRESSURE_VAL = 0x30  # 压力值暂时固定
ABS_MT_POSITION_X = 0x0035  # X坐标
ABS_MT_POSITION_Y = 0x0036  # Y坐标
ABS_MT_TRACKING_ID = 0x0039  # 多点触控时区分点
EV_SYN = 0x0000
SYN_MT_REPORT = 0x0002  # 值为0即可
SYN_REPORT = 0x0000  # 值为0即可
EV_KEY = 0x0001
BTN_TOUCH = 0x014a
BTN_TOUCH_DOWN = 0x00000001  # 按下
BTN_TOUCH_UP = 0x00000000  # 松开

########## 计算值 ##########
LEFT_DELTA_X = (LEFT_DOWN_X-LEFT_UP_X)/(PANEL_ROWS-1)
LEFT_DELTA_Y = (LEFT_DOWN_Y-LEFT_UP_Y)/(PANEL_ROWS-1)
RIGHT_DELTA_X = (RIGHT_DOWN_X-RIGHT_UP_X)/(PANEL_ROWS-1)
RIGHT_DELTA_Y = (RIGHT_DOWN_Y-RIGHT_UP_Y)/(PANEL_ROWS-1)


LEFT_DELTA_XX = (LEFT_DOWN_XX-LEFT_UP_XX)/(PANEL_ROWS-1)
LEFT_DELTA_YY = (LEFT_DOWN_YY-LEFT_UP_YY)/(PANEL_ROWS-1)
RIGHT_DELTA_XX = (RIGHT_DOWN_XX-RIGHT_UP_XX)/(PANEL_ROWS-1)
RIGHT_DELTA_YY = (RIGHT_DOWN_YY-RIGHT_UP_YY)/(PANEL_ROWS-1)


def calc_abspos(r: int, c: int) -> (int, int):
    left_x = LEFT_UP_X+r*LEFT_DELTA_X
    left_y = LEFT_UP_Y+r*LEFT_DELTA_Y
    right_x = RIGHT_UP_X+r*RIGHT_DELTA_X
    right_y = RIGHT_UP_Y+r*RIGHT_DELTA_Y
    x = round(left_x + (right_x-left_x)*c/(PANEL_COLUMNS-1))
    y = round(left_y + (right_y-left_y)*c/(PANEL_COLUMNS-1))
    return x, y


def calc_relpos(r: int, c: int) -> (int, int):
    left_x = LEFT_UP_XX+r*LEFT_DELTA_XX
    left_y = LEFT_UP_YY+r*LEFT_DELTA_YY
    right_x = RIGHT_UP_XX+r*RIGHT_DELTA_XX
    right_y = RIGHT_UP_YY+r*RIGHT_DELTA_YY
    x = round(left_x + (right_x-left_x)*c/(PANEL_COLUMNS-1))
    y = round(left_y + (right_y-left_y)*c/(PANEL_COLUMNS-1))
    return x, y


PANEL_KEYS_ABS = [[calc_abspos(r, c) for c in range(PANEL_COLUMNS)]
                  for r in range(PANEL_ROWS)]

PANEL_KEYS_REL = [[calc_relpos(r, c) for c in range(PANEL_COLUMNS)]
                  for r in range(PANEL_ROWS)]


def get_cmd_key_press(key: (int, int), id: int)->list:
    r, c = key
    x, y = PANEL_KEYS_ABS[r][c]
    return [
        f'sendevent {DEVICE} {EV_ABS} {ABS_MT_PRESSURE} {ABS_MT_PRESSURE_VAL}',
        f'sendevent {DEVICE} {EV_ABS} {ABS_MT_POSITION_X} {x}',
        f'sendevent {DEVICE} {EV_ABS} {ABS_MT_POSITION_Y} {y}',
        f'sendevent {DEVICE} {EV_ABS} {ABS_MT_TRACKING_ID} {id}',
        f'sendevent {DEVICE} {EV_SYN} {SYN_MT_REPORT} 0'
    ]


def get_cmd_keys_press(keys: list, down: bool = False) -> list:
    cmds = []
    for i, key in enumerate(keys):
        cmds.extend(get_cmd_key_press(key, i))
    if down:
        cmds.append(
            f'sendevent {DEVICE} {EV_KEY} {BTN_TOUCH} {BTN_TOUCH_DOWN}')
    cmds.append(f'sendevent {DEVICE} {EV_SYN} {SYN_REPORT} 0')
    return cmds


def get_cmd_key_up()->list:
    return [
        f'sendevent {DEVICE} {EV_SYN} {SYN_MT_REPORT} 0',
        f'sendevent {DEVICE} {EV_KEY} {BTN_TOUCH} {BTN_TOUCH_UP}',
        f'sendevent {DEVICE} {EV_SYN} {SYN_REPORT} 0'
    ]


def press(note) -> None:
    print('press:')
    if not note:
        print('')
        return
    elif type(note) == tuple:
        print(note)
        keys = [note]
    elif type(note) == set:
        pprint.pprint(note)
        keys = note
    else:
        raise Exception(f'Unknow note [{note}]')
    cmds = get_cmd_keys_press(keys, True)
    cmds.extend(get_cmd_keys_press(keys))
    cmds.extend(get_cmd_key_up())
    prefix = 'adb shell'
    for cmd in cmds:
        os.system(f'{prefix} {cmd}')


def tap(note) -> None:
    print('tap:')
    if not note:
        print('')
        return
    elif type(note) == tuple:
        print(note)
        r, c = note
        x, y = PANEL_KEYS_REL[r][c]
        cmd = f'adb shell input tap {x} {y}'
        os.system(cmd)
    elif type(note) == list:
        pprint.pprint(note)
        r, c = note[0]
        x, y = PANEL_KEYS_REL[r][c]
        cmd = f'adb shell "input tap {x} {y}'
        for key in note[1:]:
            r, c = key
            x, y = PANEL_KEYS_REL[r][c]
            cmd += f' && input tap {x} {y}'
        cmd += '"'
        os.system(cmd)
    else:
        raise Exception(f'Unknow note [{note}]')


def play(music: dict, mode: str = 'tap'):
    '''
    tap 只能单击
    sendevent需要root权限
    '''
    if 'space' not in music:
        space = DEFAULT_CLICK_SPACE
    else:
        space = music['space']
    notes = music['notes']
    for note in notes:
        pre = time.perf_counter()
        if type(note) == float:
            space = note
            continue
        if mode == 'tap':
            tap(note)
        else:
            press(note)
        wait = space+pre-time.perf_counter()
        if wait > 0:
            time.sleep(wait)


def get_music_type_A1(text: list)->dict:
    notes_to_pos = {}
    for i in range(5):
        notes_to_pos[f'A{i+1}'] = (0, i)
    for i in range(2):
        notes_to_pos[f'A{i+6}'] = (1, i)
    for i in range(3):
        notes_to_pos[f'B{i+1}'] = (1, i+2)
    for i in range(4):
        notes_to_pos[f'B{i+4}'] = (2, i)
    notes_to_pos['C1'] = (2, 4)
    music = {}
    music['space'] = float(text[0])
    text = text[1:]
    music['notes'] = []
    nowconcat = None
    nowmulti = None
    concat = False
    multi = False
    for line in text:
        if line.strip().startswith('#'):
            continue
        for word in line.split(' '):
            if not word:
                continue
            word = word.strip().upper()
            if word in notes_to_pos:
                if concat:
                    nowconcat.append(notes_to_pos[word])
                elif multi:
                    nowmulti.add(notes_to_pos[word])
                else:
                    music['notes'].append(notes_to_pos[word])
            elif word.startswith('$'):
                space = float(word[1:])
                music['notes'].append(space)
            elif word == '[':
                concat = True
                nowconcat = []
            elif word == ']':
                concat = False
                music['notes'].append(nowconcat)
            elif word == '{':
                multi = True
                nowmulti = set({})
            elif word == '}':
                multi = False
                music['notes'].append(nowmulti)
            elif word == '~':
                music['notes'].append(None)
    return music


def get_music(music_file: str) -> dict:
    '''
    music:{
        notes: 音符
        space: 间隔
    }
    '''
    with open(music_file, 'r', encoding='utf-8') as f:
        text = f.readlines()
    tp = text[0].strip()
    if tp == 'type_A1':
        return get_music_type_A1(text[1:])
    else:
        raise Exception(f'unknown type [{tp}]')


if __name__ == '__main__':
    print('by ztx97')
    print('https://github.com/zhangtianxiang')
    if len(sys.argv) > 1:
        print(f'will play {sys.argv[1]}')
        music = get_music(sys.argv[1])
    else:
        music = {}
        music['notes'] = [[(r, c)] for c in range(PANEL_COLUMNS)
                          for r in range(PANEL_ROWS)]
    play(music, PLAY_MODE)
