# Sky Music Player

光遇乐谱弹奏工具

## 这是什么

制作自己的曲子并在Sky中自动播放。诚然，这确实是在光遇中快速“掌握”弹奏技巧的方法。但我的本意是通过此脚本来学习弹奏。通过这个工具，玩家可以先谱写想要弹奏的曲子，并通过自动播放来测试曲子，最终根据对满意的曲子进行学习。

## 依赖

### 安卓设备

本工具仅适用于安卓（Android）设备。

### 安卓调试桥 (Android Debug Bridge, adb)

[https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools)

安装后应当将adb所在路径添加到环境变量PATH中。本工具将直接通过命令行指令调用adb。

### Python3

本工具由Python3语言开发。

## 安装

下载源代码解压或直接`git clone`到本地。

## 配置

1. 打开安卓设备的开发者模式并打开调试模式。

2. 使用数据线将安卓设备连接至有adb的电脑，在安卓设备上允许调试。

3. 打开光遇，调出弹奏界面。

4. 分为两种情况：
   1. tap模式：将使用`adb shell input tap`指令模拟点击，无需root，缺点是响应速度慢，只允许单点触控。如果使用tap模式自动弹奏，则需要使用命令行`adb shell input tap X Y`来手动定位15个键中左上、左下、右上、右下四个键的坐标。在配置文件`config.py`中将`PLAY_MODE`赋值为`'tap'`，并将四点坐标填入对应位置。
   2. sendevent模式：将使用`adb shell sendevent`指令模拟点击，需要root，允许多点触控。如果使用sendevent模式自动弹奏，则需要使用命令行`adb shell getevent -l`监听安卓设备屏幕点击事件。分别点左上、左下、右上、右下四个键，命令行中会显示点击事件，将其中的`ABS_MT_POSITION_X`、`ABS_MT_POSITION_Y`记录下来填入配置文件`config.py`中，将`PLAY_MODE`赋值为`'sendevent'`。最后使用`Ctrl+C`结束`getevent`命令。`getevent`显示的`X`、`Y`值都是十六进制数，在填写时记得转为十进制或者前面加上`0x`。`getevent`显示的事件总是以形如`/dev/input/eventX`作为前缀，这个前缀记录下来赋值给`DEVICE`。

## 使用

1. 使用数据线将安卓设备连接至有adb的电脑，在安卓设备上允许调试。

2. 打开光遇，调出弹奏界面。

3. 编写乐谱文件或使用已有的乐谱文件。

4. 执行`python3 play.py MUSIC_FILE.txt`。其中`MUSIC_FILE.txt`即为乐谱文件的文件名。

## 乐谱格式

目前只支持type_A1类型的乐谱

### type_A1

- 第一行为type_A1
- 第二行为默认时间间隔（秒）
- 剩余行全部被解析为音符。音符支持 a1-a7 b1-b7 c1 ‘\~’，其中a1-a7代表着前7个键，b1-b7代表中间7个键，c1代表最后一行的最后一个键，\~ 代表不发音。大小写不敏感。
- ‘#’开头的行将被忽略
- 不被识别的符号将被忽略
- 以中括号（\[\]）括起来的音符，将被以0秒间隔顺序点击（实际上由于adb指令的延迟，时间间隔仍然较大，可自行体会，sendevent不支持此形式的音符）。注意括号不要与音符连接起来。
- 以花括号（{}）括起来的音符，将被同时点击（tap不支持此形式的音符，由于我的设备没有root，也没有进行测试）。注意括号不要与音符连接起来。
- 以`$`开头的小数将改变此位置开始后面音符的时间间隔，如`$0.6`表明由此开始，后面音符间隔0.6秒。

例：[`大鱼.txt`](./大鱼.txt)。

## 进一步开发

可以扩展更多的乐谱格式，欢迎issue和pr。
