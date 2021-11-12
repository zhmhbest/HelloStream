from ffmpeg.FFBaseCommand import FFBaseCommand


class FFEasyCommand(FFBaseCommand):
    def __init__(self, mpeg_location: str = "ffmpeg", play_location: str = "ffplay", probe_location: str = "ffprobe"):
        FFBaseCommand.__init__(self, mpeg_location, play_location, probe_location)

    def play(self, src: str, title='', shape=None, loop=0):
        """
        播放视频
        :param src:
        :param title:
        :param shape: 窗口尺寸
        :param loop: 循环几次，0表示一直循环
        :return:
        """
        if shape is None:
            self.ffplay([src, '-window_title', title, '-loop', str(loop)])
        else:
            self.ffplay([src, '-x', str(shape[0]), '-y', str(shape[1]), '-window_title', title, '-loop', str(loop)])

    def msg_video(self, src: str):
        """
        查看视频的视频信息
        :param src:
        :return:
        """
        self.ffprobe(['-v', 'quiet', '-show_streams', '-select_streams', 'v', '-i', src])

    def msg_audio(self, src: str):
        """
        查看视频的音频信息
        :param src:
        :return:
        """
        self.ffprobe(['-v', 'quiet', '-show_streams', '-select_streams', 'a', '-i', src])

    def detach(self, src: str, path_to_video=None, path_to_audio=None):
        """
        分离视频和音频
        :param src: 视频文件
        :param path_to_video: 导出视频位置
        :param path_to_audio: 导出音频位置
        :return:
        """
        if path_to_video is not None:
            # 分离出视频
            self.ffmpeg(['-i', src, '-vcodec', 'copy', '-an', f'{path_to_video}.264'])
        if path_to_audio is not None:
            # 分离出音频
            self.ffmpeg(['-i', src, '-vcodec', 'copy', '-vn', f'{path_to_audio}.aac'])

    def repack(self, srcs: str or [str, ...], path_to_save: str):
        """
        重新封装视频 或 合并视频和音频
        :param srcs:
        :param path_to_save:
        :return:
        """
        cmd = []
        if isinstance(srcs, list):
            for src in srcs:
                cmd.append('-i')
                cmd.append(src)
        else:
            cmd.append('-i')
            cmd.append(srcs)
        cmd.extend(['-vcodec', 'copy', '-acodec', 'copy', path_to_save])
        self.ffmpeg(cmd)

    def cut_key(self, src: str, start_time, duration_or_end_time, output: str):
        """
        关键帧裁剪视频
        但会造成几秒的误差，只能落在关键帧上
        :param src:
        :param start_time: 开始时间
        :param duration_or_end_time: 持续时间 或 结束时间
        :param output:
        :return:
        """
        self.ffmpeg([
            '-i', src,
            '-ss', start_time,
            '-to' if isinstance(duration_or_end_time, str) else '-t', str(duration_or_end_time),
            # '-vcodec', 'copy', '-acodec', 'copy',
            '-codec', 'copy',
            output, '-y'
        ])

    def cut_acc(self, src: str, start_time, duration_or_end_time, output: str):
        """
        精准裁剪
        :param src:
        :param start_time: 开始时间
        :param duration_or_end_time: 持续时间 或 结束时间
        :param output:
        :return:
        """
        self.ffmpeg([
            '-ss', start_time,
            '-to' if isinstance(duration_or_end_time, str) else '-t', str(duration_or_end_time),
            '-accurate_seek',
            '-i', src,
            # '-vcodec', 'copy', '-acodec', 'copy',
            '-codec', 'copy',
            '-avoid_negative_ts', '1',
            output, '-y'
        ])

    def combine(self, src_list: list, output: str):
        """
        合并多个视频
        :param src_list: [视频地址1, 视频地址2, ...]
        :param output: 输出地址
        :return:
        """
        import random
        import os
        dump_list_file = os.path.abspath(f"{output}.{random.random()}.dump_list.txt")
        with open(dump_list_file, 'w') as fp:
            for item in src_list:
                item = os.path.abspath(item).replace('\\', '/')
                fp.write(f"file {item}\n")
        self.ffmpeg([
            '-f', 'concat',
            '-safe', '0',
            '-i', dump_list_file,
            '-codec', 'copy',
            '-y', output
        ])
        os.remove(dump_list_file)

    def encode_audio(
            self,
            src_audio: str, output: str, to_format: str,
            acodec: str = None,
            brc: (int, int, int) = None
    ):
        """
        编码Audio
        :param src_audio: 音频文件地址
        :param output: 输出地址
        :param to_format: 编码为, eg: mp3、ogg、wave、flac
        :param acodec: 编码, eg: copy、pcm_s24le、libmp3lame
        :param brc: (ab, ar, ac)
            ab: 码率, eg: 128
            ar: 采样率, eg: 16
            ac: 声道, eg: 2
        :return:
        """
        cmd = ['-i', src_audio]
        # 设置编码器
        if acodec is not None:
            cmd.extend(['-acodec', acodec])
        # 设置码率
        if brc is not None and 3 == len(brc):
            cmd.extend([
                '-ab', f'{str(brc[0])}k',
                '-ar', f'{str(brc[1])}k',
                '-ac', str(brc[2]),
            ])
        # 设置格式
        cmd.extend(['-f', to_format, '-y', output])
        self.ffmpeg(cmd)

    def encode_video_crf(
            self,
            src_video: str, output: str, crf: int
    ):
        """
        编码视频ByCRF
        :param src_video: 视频文件地址
        :param output: 输出地址
        :param crf: Constant Rate Factor{0 ~ 51}, advance{18 ~ 28}, 越大越差
        :return:
        """
        cmd = ['-i', src_video, '-vcodec', 'libx264', '-acodec', 'copy']
        cmd.extend(['-crf', str(crf)])
        cmd.extend(['-f', 'mp4', '-y', output])
        self.ffmpeg(cmd)

    def encode_video_2pass(
            self,
            src_video: str, output: str,
            vb: int
    ):
        """
        编码视频By2Pass
        :param src_video: 视频文件地址
        :param output: 输出地址
        :param vb: 比特率大小，越大视频越清晰，占用更大空间
        :return:
        """
        cmd = ['-i', src_video, '-vcodec', 'libx264', '-vb', f'{vb}k']
        cmd1 = cmd.copy()
        cmd1.extend(['-an', '-pass', '1', '-f', 'mp4', '-y', 'NUL'])
        self.ffmpeg(cmd1)
        cmd2 = cmd.copy()
        cmd2.extend(['-acodec', 'copy', '-pass', '2', '-f', 'mp4', '-y', output])
        self.ffmpeg(cmd2)


if __name__ == '__main__':
    ff = FFEasyCommand()
