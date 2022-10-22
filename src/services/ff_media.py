from schemas import MediaInfoSchema
import ffmpeg
from pathlib import Path
import subprocess
import io
from settings import settings
from prefect import get_run_logger
import re


class MediaServicesFF:

    schema = MediaInfoSchema

    def __init__(self, file_path):
        self.file_path = file_path
        self.probe = ffmpeg.probe(file_path)

    async def convert(self, size):
        logger = get_run_logger()

        name_file = Path(self.format.get('filename')).name
        new_file = settings.temporary_dir / f'{size}_{name_file}'

        cmd = ['ffmpeg', '-i', self.file_path, '-s', size, new_file]
        process = subprocess.Popen(
            cmd,
            shell=False,
            stderr=subprocess.PIPE,
            universal_newlines=False,
        )
        reader = io.TextIOWrapper(process.stderr, newline=None)

        while process.poll() is None:
            line = reader.readline()
            try:
                time_str = re.compile(r'time=(\d+:\d+:\d+.\d+) ').findall(line)[0]
            except IndexError:
                continue
            time: float = 0
            for part in time_str.split(':'):
                time = 60 * time + float(part)

            percent = round(time / float(self.format.get('duration')) * 100, 2)
            logger.info(f'{name_file} scaling {size} {percent} %')

        return new_file

    @property
    def video(self):
        return next((stream for stream in self.probe['streams'] if stream['codec_type'] == 'video'), None)

    @property
    def audio(self):
        return next((stream for stream in self.probe['streams'] if stream['codec_type'] == 'audio'), None)

    @property
    def format(self):
        return self.probe.get('format', None)

    @property
    def short_info(self):
        return self.schema(
            width=self.video.get('width'),
            height=self.video.get('height'),
            vcodec=self.video.get('codec_name'),
            acodec=self.audio.get('codec_name'),
            duration=self.format.get('duration'),
            format=self.format.get('format_name'),
            filename=Path(self.format.get('filename')).name,
        )
