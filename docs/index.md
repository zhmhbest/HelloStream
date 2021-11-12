<link rel="stylesheet" href="https://zhmhbest.gitee.io/hellomathematics/style/index.css">
<script src="https://zhmhbest.gitee.io/hellomathematics/style/index.js"></script>

# [FFMpeg](https://github.com/zhmhbest/HelloStream)

[TOC]

## 下载

- [Download FFmpeg](http://www.ffmpeg.org/download.html)

<!--
- [Download FFmpeg Builds](https://ffmpeg.zeranoe.com/builds/)
- [FFmpeg Builds Release Win64](https://ffmpeg.zeranoe.com/builds/win64/)
- [FFmpeg Builds Release Win32](https://ffmpeg.zeranoe.com/builds/win32/)
- [FFmpeg Builds Release MacOS64](https://ffmpeg.zeranoe.com/builds/macos64/)
-->

## Play

```bash
# 播放视频
ffplay "${VideoSource}" [-x "${窗口宽度}"] [-y "${窗口高度}"] -window_title "${标题}" -loop "${循环几次}"
```

## Probe

```bash
# 文件信息
ffprobe "${VideoSource}"

# 视频信息
ffprobe -v quiet -show_streams -select_streams v -i "${VideoSource}"

# 音频信息
ffprobe -v quiet -show_streams -select_streams a -i "${VideoSource}"
```

## Mpeg

>[FFMpeg Document](https://ffmpeg.org/ffmpeg-all.html)
>[JSMpeg Document](https://hub.fastgit.org/phoboslab/jsmpeg)

### 概述

>I帧：关键帧
>P帧：帧间预测编码帧
>B帧：双向预测编码帧

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

```bash
ffmpeg
    -c <编解码器> | -codec <编解码器>
    -b <CBR比特率>
    -q <VBR质量> # -1.0~10.0
    -threads <线程数>
    -thread_type <多线程类型> # slice | frame

    # 输入源
    -rtsp_transport <协议类型> # http | udp | tcp
    -i <输入源或文件列表>
    -video_size <抓取视频帧大小> # eg: vga cif hd720
    -re # 以本机帧速率读取输入
    -framerate <抓取帧速率> # eg: 1 6 10

    -sn # 禁用字幕
    -c:s <字幕编解码器> | -codec:s <字幕编解码器> | -scodec <字幕编解码器>

    -vn # 禁用视频源
    -c:v <视频编解码器> | -codec:v <视频编解码器> | -vcodec <视频编解码器>
    -b:v <视频码率> | -vb <视频码率> # eg: 1150k
    -s      <视频窗口大小> # eg: 352x288
    -aspect <视频宽高比> # eg: 4:3 16:9
    -r      <视频固定帧率> # eg: 24
    -fpsmax <最大帧速率>
    -g      <关键帧间隔> # eg: 300
    -bf     <B帧数目控制> # eg: 2
    -q:v    <VBR视频质量> # eg: 3.0

    # libx264
    -crf    <固定码率因子> # 18~28
    -pass   <PASS次数> # 1~2

    -an # 禁用音频源
    -c:a <音频编解码器> | -codec:a <音频编解码器> | -acodec <音频编解码器>
    -b:a <音频码率> | -ab <音频码率># eg: 128K
    -ar <音频采样率> # eg: 22050
    -ac <音频声道> # eg: 2
    -vol <音量> # eg: 100
    -q:a <VBR音频质量> | -aq <VBR音频质量>

    -accurate_seek | -noaccurate_seek # 是否启用精确寻找
    -ss <开始位置>
    -to <结束位置> | -t <持续时间>

    -f <输出格式> # eg: mp4 | flv | avi
    -target <目标> # eg: vcd | svcd | dvd | dv | dv50
    -y # 覆盖输出文件
    <输出位置>
```

### 可用

```bash
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

### 拆封

```bash
# 分离出视频
ffmpeg -i "${VideoSource}" -c:v copy -an "${VideoOutputPath}.264"

# 分离出音频
ffmpeg -i "${VideoSource}" -c:a copy -vn "${AudioOutputPath}.aac"

# 封装视音频
ffmpeg -i "${VideoSource}" -i "${AudioSource}" -c copy "${VideoOutputPath}.mp4"
```

### 裁剪

```bash
# 关键帧裁剪视频：会造成几秒的误差，只能落在关键帧上
ffmpeg -i "${VideoSource}" -ss "${开始时间}" {-to "${结束时间}" | -t "${持续时间}"} -c copy -y "${VideoOutputPath}.mp4"

# 精准裁剪
ffmpeg -i "${VideoSource}" -ss "${开始时间}" {-to "${结束时间}" | -t "${持续时间}"} -accurate_seek -c copy -avoid_negative_ts 1 -y "${VideoOutputPath}.mp4"
```

### 合并

`FileList.txt`

```txt
file 0.ts
file 1.ts
...
```

```bash
ffmpeg -f concat -safe 0 -i FileList.txt -c copy -y "${VideoOutputPath}.mp4"
```

### 转码

```bash
# 编码Audio
ffmpeg -i "${AudioSource}" -c:a {copy | pcm_s24le | libmp3lame} -b:a "${码率}" -ar "${采样率}" -ac "${声道}" -y "${结果保存地址}.{mp3 | ogg | wave | flac}"

# 编码视频——CRF
ffmpeg -i "${VideoSource}" -c:v libx264 -c:a copy -crf "${固定码率因子}" -f mp4 "${结果保存地址}.mp4"

# 编码视频——2Pass
ffmpeg -i "${VideoSource}" -vcodec libx264 -b:v "${比特率大小}" -an -pass 1 -f mp4 -y NUL
ffmpeg -i "${VideoSource}" -vcodec libx264 -b:v "${比特率大小}" -c:a copy -pass 2 -y "${结果保存地址}.mp4"
```

### 实时

```bash
# 获取实时流保存到本地

# 43k/s
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
    disableWebAssembly: true,
    disableGl: true,
    video: true,
    audio: false,
    autoplay: true,
    loop: false
})
```
