<link rel="stylesheet" href="https://zhmhbest.gitee.io/hellomathematics/style/index.css">
<script src="https://zhmhbest.gitee.io/hellomathematics/style/index.js"></script>

# [Stream](https://github.com/zhmhbest/HelloStream)

[TOC]

## 相关概念

### 帧

- I帧：关键帧
- P帧：帧间预测编码帧
- B帧：双向预测编码帧

### 编码格式

如何编码视音频信息。例如：`MPEG-4`、`H.264`、`H.265`、`ACC`、`PCM`等均为编码格式。

### 封装格式

如何存储编码后的视音频信息，将视频、音频、字幕等封装进一个文件。例如:`mp4`、`flv`、`avi`、`mp3`、`ogg`等均为封装格式。

## FFMpeg

- [Download FFmpeg](http://www.ffmpeg.org/download.html)

### Play

```bash
# 播放视频
ffplay
    <视音频源>
    [-x <画面宽度>] [-y <画面高度>]
    [-window_title <窗口标题>]
    [-loop <循环次数>]
```

### Probe

```bash
# 文件信息
ffprobe <视音频源>

# 视频信息
ffprobe -v quiet -show_streams -select_streams v -i <视频源>

# 音频信息
ffprobe -v quiet -show_streams -select_streams a -i <音频源>
```

### Mpeg

>[FFMpeg Document](https://ffmpeg.org/ffmpeg-all.html)
>[JSMpeg Document](https://hub.fastgit.org/phoboslab/jsmpeg)

```txt
 _______              ______________
|       |            |              |
| input |  demuxer   | encoded data |   decoder
| file  | ---------> | packets      | -----+
|_______|            |______________|      |
                                           v
                                       _________
                                      |         |
                                      | decoded |
                                      | frames  |
                                      |_________|
 ________             ______________       |
|        |           |              |      |
| output | <-------- | encoded data | <----+
| file   |   muxer   | packets      |   encoder
|________|           |______________|
```

```bnf
ffmpeg
    # -c <编解码器> | -codec <编解码器>
    # -b <CBR比特率>
    # -q <VBR质量> # -1.0~10.0

    -threads <线程数>
    -thread_type <多线程类型> # slice | frame

    # 【输入】
    -rtsp_transport <输入协议> # http | udp | tcp
    -re # 以本地帧频读数据
    -video_size <抓取窗口大小> # eg: vga cif hd720
    -framerate <抓取帧速率> # eg: 1 6 10
    -i <输入源或文件列表>
    -f <输入格式>

    # 【字母】
    -sn # 禁用字幕
    -c:s <字幕编解码器> | -codec:s <字幕编解码器> | -scodec <字幕编解码器>

    # 【视频】
    -vn # 禁用视频源
    -c:v <视频编解码器> | -codec:v <视频编解码器> | -vcodec <视频编解码器>
    -b:v <视频码率> | -vb <视频码率> # eg: 1150k
    -q:v    <VBR视频质量> # eg: 3.0
    -r      <视频固定帧率> # eg: 24
    -s      <视频窗口大小> # eg: 352x288
    -aspect <视频宽高比> # eg: 4:3 16:9
    #
    -g      <关键帧间隔> # eg: 300
    -bf     <B帧数目控制> # eg: 2
    # libx264
    -crf    <固定码率因子> # 18~28
    -pass   <PASS次数> # 1~2

    # 【音频】
    -an # 禁用音频源
    -c:a <音频编解码器> | -codec:a <音频编解码器> | -acodec <音频编解码器>
    -b:a <音频码率> | -ab <音频码率># eg: 128K
    -ar <音频采样率> # eg: 22050
    -ac <音频声道> # eg: 2
    -vol <音量> # eg: 100
    -q:a <VBR音频质量> | -aq <VBR音频质量>

    # 【位置】
    -accurate_seek | -noaccurate_seek # 是否启用精确寻找
    -ss <开始位置>
    -to <结束位置> | -t <持续时间>

    # 【输出】
    -target <目标> # eg: vcd | svcd | dvd | dv | dv50
    -y # 覆盖输出文件
    <输出位置>
```

#### 可用

```bnf
# 列出所有可用封装格式
ffmpeg -formats

# 列出所有可用muxers
ffmpeg -muxers
ffmpeg -demuxers

# 列出所有可用设备
ffmpeg -devices

# 列出所有可用协议
ffmpeg -protocols

# 列出所有编码解码器
ffmpeg -codecs
ffmpeg -encoders
ffmpeg -decoders

# 列出所有libavfilter已知的过滤器
ffmpeg -filters

# 列出所有可用比特流过滤器
ffmpeg -bsfs

# 列出所有可用的像素格式
ffmpeg -pix_fmts

# 列出所有可用的采样格式
ffmpeg -sample_fmts

# 列出所有可用的Channel名称和标准布局
ffmpeg -layouts

# 列出所有识别的颜色名称
ffmpeg -colors
```

#### 拆封

```bnf
# 分离出视频
ffmpeg -i <视频源> -c:v copy -an <输出>.264

# 分离出音频
ffmpeg -i <视频源> -c:a copy -vn <输出>.aac

# 封装视音频
ffmpeg -i <视频源> -i <音频源> -c copy <输出>.mp4
```

#### 裁剪

```bnf
# 关键帧裁剪视频：会造成几秒的误差，只能落在关键帧上
ffmpeg -i <视频源> -ss <开始时间> {-to <结束时间> | -t <持续时间>} -c copy -y <输出>.mp4

# 精准裁剪
ffmpeg -i <视频源> -ss <开始时间> {-to <结束时间> | -t <持续时间>} -accurate_seek -c copy -avoid_negative_ts 1 -y <输出>.mp4
```

#### 合并

`FileList.txt`

```txt
file 0.ts
file 1.ts
...
```

```bnf
ffmpeg -f concat -safe 0 -i FileList.txt -c copy -y <输出>.mp4
```

#### 转码

```bnf
# 编码Audio
ffmpeg -i <音频源> -c:a {copy | pcm_s24le | libmp3lame} -b:a <码率> -ar <采样率> -ac <声道> -y <输出>.{mp3 | ogg | wave | flac}

# 编码视频——CRF
ffmpeg -i <视频源> -c:v libx264 -c:a copy -crf <固定码率因子> -f mp4 <输出>.mp4

# 编码视频——2Pass
ffmpeg -i <视频源> -vcodec libx264 -b:v <比特率大小> -an -pass 1 -f mp4 -y NUL
ffmpeg -i <视频源> -vcodec libx264 -b:v <比特率大小> -c:a copy -pass 2 -y <输出>.mp4
```

#### 实时

```bnf
# 获取实时流保存到本地
ffmpeg \
    -threads 4 \
    -re \
    -rtsp_transport tcp \
    -i "rtsp://..." \
    -f mpegts \
    -fflags nobuffer \
    -r 24 \
    -q:v 8.0 \
    -c:v mpeg1video \
    -s 960x469 \
    -an \
    r.mp4
```

```js
// JS播放实时流
let player = new window.JSMpeg.Player(url, {
    canvas: canvas, // <canvas></canvas>
    progressive: true,
    chunkSize: 256 * 1024, // 32K
    decodeFirstFrame: false,
    disableWebAssembly: false,
    disableGl: true,
    video: true,
    audio: false,
    autoplay: true,
    loop: false
})
```
