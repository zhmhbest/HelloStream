import subprocess
from typing import List


class FFBaseCommand:
    # @staticmethod
    # def check_files_exist(files: List[str]):
    #     for file in files:
    #         if not os.path.exists(file):
    #             raise FileNotFoundError(file)

    def __init__(self, mpeg_location: str = "ffmpeg", play_location: str = "ffplay", probe_location: str = "ffprobe"):
        self.bin_mpeg = mpeg_location
        self.bin_play = play_location
        self.bin_probe = probe_location

    def ffmpeg(self, args: List[str]):
        args.insert(0, self.bin_mpeg)
        subprocess.run(args)

    def ffplay(self, args: List[str]):
        args.insert(0, self.bin_play)
        subprocess.run(args)

    def ffprobe(self, args: List[str]):
        args.insert(0, self.bin_probe)
        subprocess.run(args)


if __name__ == '__main__':
    ff = FFBaseCommand()
    # video_file = "/home/zhmhbest/share/E/Userprofile/Videos/星尘史诗.mp4"
    video_file = r"E:\Userprofile\Videos\星尘史诗.mp4"
    ff.play([video_file])
