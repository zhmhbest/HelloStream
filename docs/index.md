<link rel="stylesheet" href="https://zhmhbest.gitee.io/hellomathematics/style/index.css">
<script src="https://zhmhbest.gitee.io/hellomathematics/style/index.js"></script>

# [Stream](https://github.com/zhmhbest/HelloStream)

[TOC]

## 概念

### 基本概念

#### 视频帧

|       概念 | 说明                               |
| ---------: | :--------------------------------- |
| **分辨率** | 视频宽高，用于衡量每帧像素数量     |
|   **码率** | 比特每秒，用于衡量视频大小和清晰度 |
|   **帧率** | 帧数每秒，用于衡量视频的连贯性     |
|    **I帧** | 关键帧                             |
|    **P帧** | 帧间预测编码帧                     |
|    **B帧** | 双向预测编码帧                     |

#### 编码格式

如何编码视音频信息。

例如：`MPEG-4`、`H.264`、`H.265`、`ACC`、`PCM`等均为编码格式。

#### 封装格式

如何存储编码后的视音频信息，将视频、音频、字幕等封装进一个文件。

例如：`mp4`、`flv`、`f4v`、`avi`、`rmvb`、`mp3`、`ogg`等均为封装格式。

#### 视频协议

视频如何在网络中传输，视频协议可以看作是一种特殊的视频**封装格式**。

|   协议 |   公司   | 实时效果 | 浏览器兼容 | 特点                                             |
| -----: | :------: | :------: | ---------: | ------------------------------------------------ |
|  `hls` |  Apple   |    差    |         好 | 流媒体切片，切片信息保存到m3u列表传输            |
| `rtmp` |  Adobe   |  低延迟  |  需要Flash | 一般使用`flv`、`f4v`封装，需要Flash插件播放      |
| `rtsp` | Netscape |  非常好  |   需要插件 | 命令和数据通道分离，基于文本的多媒体播放控制协议 |

### 相关工具

- [FFmpeg](https://ffmpeg.org/ffmpeg-all.html)：跨平台视频流转码解决方案
- [JSMpeg](https://jsmpeg.com/)：前端视频流播放解决方案

## FFMpeg

FFMpeg包含`ffplay`、`ffprobe`、`ffmpeg`三个主要文件。

### Play

`ffplay [OPTIONS] INPUT_FILE`

```abnf
; OPTIONS
    -x <显示宽度>
    -y <显示高度>
    -s <画面宽度>x<画面高度>
    -an ; 关闭视频
    -vn ; 关闭音频
    -sn ; 关闭字幕
    -volume <声音大小>
    -window_title <窗口标题>
    -loop <循环次数>
```

```bash
# demo
ffplay -loop 1 video.mp4
```

### Probe

`ffprobe [OPTIONS] [INPUT_FILE]`

```abnf
; OPTIONS
    -v quiet/panic/fatal/error/warning/info/verbose/debug/trace ; 日志等级
    -show_streams [-select_streams v/a]
```

```bash
# demo
ffprobe -v quiet -show_streams -select_streams v video.mp4
```

### Mpeg

`ffmpeg [OPTIONS] [INPUT_OPTIONS] -i INPUT_FILE [OUTPUT_OPTIONS] OUTPUT_FILE`

```abnf
; OPTIONS
    -threads <线程数>
    -thread_type slice/frame ; 多线程类型
```

```abnf
; INPUT_OPTIONS/OUTPUT_OPTIONS
    ; -c/-codec <编解码器>
    ; -b <CBR比特率>
    ; -q <VBR质量> ; -1.0~10.0

    -rtsp_transport http/udp/tcp

    ; 【字幕】
    -sn ; 禁用字幕
    -c:s/-codec:s/-scodec <字幕编解码器>

    ; 【视频】
    -vn ; 禁用视频源
    -c:v/-codec:v/-vcodec <视频编解码器>
    -q:v    <VBR视频质量>       ; eg: 3.0
    -b:v/-vb <视频码率>         ; eg: 1150k
    -re ; 以本地帧频读数据
    -r/-framerate   <帧率> ; eg: 24
    -s              <窗口> ; eg: 352x288
    -aspect         <比例>  ; eg: 4:3 16:9
    -g              <关键帧间隔>    ; eg: 300
    -bf             <B帧数目控制>   ; eg: 2
    ; libx264
    -crf    <固定码率因子> ; 18~28
    -pass   1/2

    ; 【音频】
    -an ; 禁用音频源
    -c:a/-codec:a/-acodec <音频编解码器>
    -q:a/-aq <VBR音频质量>
    -b:a/-ab <码率> ; eg: 128K
    -ar      <采样> ; eg: 22050
    -ac      <声道> ; eg: 2
    -vol     <音量> ; eg: 100

    ; 【位置】
    -accurate_seek/-noaccurate_seek ; 是否启用精确寻找
    -ss <开始位置>
    -to <结束位置>
    -t  <持续时间>

    -f <封装格式>
```

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

#### 应用

**分离视音频**：

```bash
# 分离出视频
ffmpeg -i video.mp4 -c:v copy -an video.264

# 分离出音频
ffmpeg -i video.mp4 -c:a copy -vn audio.aac

# 封装视音频
ffmpeg -i video.264 -i audio.aac -c copy target.mp4
```

**裁剪视音频**：

```bash
# 关键帧裁剪视频：会造成几秒的误差，只能落在关键帧上
ffmpeg -i video.mp4 -ss 00:00:00 -to 00:10:00 -c copy -y target.mp4
ffmpeg -i video.mp4 -ss 00:00:00 -t 10 -c copy -y target.mp4

# 精准裁剪
ffmpeg -i video.mp4 -ss 00:00:00 -to 00:10:00 -accurate_seek -c copy -avoid_negative_ts 1 -y target.mp4
ffmpeg -i video.mp4 -ss 00:00:00 -t 10 -accurate_seek -c copy -avoid_negative_ts 1 -y target.mp4
```

**合并视频碎片**：

`FileList.txt`

```txt
file 0.ts
file 1.ts
...
```

```bash
ffmpeg -f concat -safe 0 -i FileList.txt -c copy -y target.mp4
```

**音频转码**：

```bash
# 编码Audio
# acodec: copy | pcm_s24le | libmp3lame
# format: mp3 | ogg | wave | flac
ffmpeg -i audio.mp3 -c:a libmp3lame -b:a 128K -ar 22050 -ac 2 -y target.mp3
```

**视频转码**：

```bash
# 编码视频——CRF
# -crf 决定视频质量和大小
ffmpeg -i video.mp4 -c:v libx264 -c:a copy -crf 1150k target.mp4

# 编码视频——2Pass
# -b:v 决定视频质量和大小
ffmpeg -i video.mp4 -vcodec libx264 -b:v 3.0 -an -pass 1 -f mp4 -y NUL
ffmpeg -i video.mp4 -vcodec libx264 -b:v 3.0 -c:a copy -pass 2 -y target.mp4
```

**本地视频推流**：

```bash
# 创建RTP流服务
ffmpeg -re -i video.mp4 -c:v mpeg1video -an -r 24 -s 960x469 -q:v 8.0 -f rtp rtp://127.0.0.1:1234

# 播放RTP流
ffplay -protocol_whitelist "udp,rtp" -i rtp://127.0.0.1:1234
```

**浏览器视频推流**：

```bash
# 推送视频到指定服务地址
ffmpeg -re -i video.mp4 -c:v mpeg1video -f mpegts -an -r 24 -s 1366x768 -q:v 8.0 http://127.0.0.1:1234/stream
```

@import "src/jsmpeg.html" {code_block=true}
