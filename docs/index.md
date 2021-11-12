<link rel="stylesheet" href="https://zhmhbest.gitee.io/hellomathematics/style/index.css">
<script src="https://zhmhbest.gitee.io/hellomathematics/style/index.js"></script>

# FFMpeg

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

### 拆封

```bash
# 分离出视频
ffmpeg -i "${VideoSource}" -vcodec copy -an "${视频流保存地址}.264"

# 分离出音频
ffmpeg -i "${VideoSource}" -vcodec copy -vn "${视频流保存地址}.aac"

# 封装视音频
ffmpeg -i "${VideoSource}" -i "${AudioSource}" -vcodec  -acodec copy "${结果保存地址}.mp4"
```

### 裁剪

```bash
# 关键帧裁剪视频：会造成几秒的误差，只能落在关键帧上
ffmpeg -i "${VideoSource}" -ss "${开始时间}" {-to "${结束时间}" | -t "${持续时间}"} -codec copy "${结果保存地址}.mp4" -y

# 精准裁剪
ffmpeg -ss "${开始时间}" {-to "${结束时间}" | -t "${持续时间}"} -accurate_seek -i "${VideoSource}" -codec copy -avoid_negative_ts 1 "${结果保存地址}.mp4" -y
```

### 合并

`FileList.txt`

```txt
file 0.ts
file 1.ts
...
```

```bash
ffmpeg -f concat -safe 0 -i FileList.txt -codec copy -y "${结果保存地址}.mp4"
```

### 转码

```bash
# 编码Audio
ffmpeg -i "${AudioSource}" -acodec {copy | pcm_s24le | libmp3lame} -ab "${码率}" -ar "${采样率}" -ac "${声道}" -f {mp3 | ogg | wave | flac} -y "${结果保存地址}.?"

# 编码视频ByCRF
ffmpeg -i "${VideoSource}" -vcodec libx264 -acodec copy -crf "${固定码率因子}" -f mp4 "${结果保存地址}.mp4"

# 编码视频By2Pass
ffmpeg -i "${VideoSource}" -vcodec libx264 -vb "${比特率大小}" -an -pass 1 -f mp4 -y NUL
ffmpeg -i "${VideoSource}" -vcodec libx264 -vb "${比特率大小}" -acodec copy -pass 2 -f mp4 -y "${结果保存地址}.mp4"
```
