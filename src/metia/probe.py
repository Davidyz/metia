import os
import json
import subprocess
from typing import Dict, Union, Optional


FFPROBE_COMMAND: str = "ffprobe"


class Probe:
    def __init__(self, path: str, encoding: str = "utf-8"):
        """
        Initialize FFprobe object.
        This requires ffprobe command added to your $PATH.
        To specify the path to ffprobe binary, change the value of metia.FFPROBE_COMMAND.
        path: path of video/audio file
        encoding: encoding of command line output. Default is utf-8.
        """
        path = os.path.realpath(os.path.expanduser(path))
        if not os.path.isfile(path):
            raise FileNotFoundError("File not found: {}".format(path))
        self.__path = path
        self.__meta = {}
        self._init(encoding)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return json.dumps(self.__meta, indent=4)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Probe):
            return hash(self) == hash(other)
        elif isinstance(other, dict):
            return self.__meta == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def dict(self):
        """
        Return the dict returned by the json parser.
        """
        return self.__meta.copy()

    def _init(self, encoding="utf8"):
        command = '{} -v quiet -hide_banner -print_format json -show_format -show_streams "{}"'.format(
            FFPROBE_COMMAND, self.__path
        )
        output = subprocess.check_output(command, shell=True)
        self.__meta = json.loads(output.decode(encoding))

    def get_tags(self) -> Optional[Dict[str, str]]:
        if self.__meta.get("format") and self.__meta["format"].get("tags"):
            return self.__meta["format"]["tags"]

    def get_tag(self, key: str) -> Optional[str]:
        if self.__meta.get("format") and self.__meta["format"].get("tags"):
            return self.__meta["format"]["tags"].get(
                key.upper()
            ) or self.__meta["format"]["tags"].get(key.lower())

    @property
    def path(self):
        return os.path.realpath(self.__path)

    def audio_codec(self) -> Dict[int, str]:
        """
        Return a dictionary of audio codecs.
        key: index of stream
        value: codec name
        """
        codecs = {}
        for stream in self.__meta["streams"]:
            if stream["codec_type"] == "audio":
                codecs[stream["index"]] = stream["codec_name"]
        return codecs

    def video_codec(self) -> Dict[int, str]:
        """
        Return a dictionary of video codecs.
        key: index of stream
        value: codec name
        """
        codecs = {}
        for stream in self.__meta["streams"]:
            if stream["codec_type"] == "video":
                codecs[stream["index"]] = stream["codec_name"]
        return codecs

    def audio_bitrates(self) -> Union[Optional[int], Dict[int, str]]:
        """
        Return a dictionary of audio bitrates.
        key: index of stream
        value: bitrate (in bps)
        """
        bitrates = {}
        for stream in self.__meta["streams"]:
            if stream["codec_type"] == "audio":
                try:
                    bitrates[stream["index"]] = int(stream["bit_rate"])
                except KeyError:
                    continue

        if bitrates == {} and self.video_codec() != {}:
            return self.__bitrate()
        return bitrates

    def video_bitrates(self) -> Dict[int, int]:
        """
        Return a dictionary of video bitrates.
        key: index of stream
        value: bitrate (in bps)
        """
        bitrates = {}
        for stream in self.__meta["streams"]:
            if stream["codec_type"] == "video":
                try:
                    bitrates[stream["index"]] = int(stream["bit_rate"])
                except KeyError:
                    continue
        if (
            bitrates == {}
            and self.video_codec() != {}
            and isinstance(self.__bitrate(), int)
        ):
            return {0: self.__bitrate()}
        return bitrates

    def __bitrate(self) -> Optional[int]:
        if (
            self.__meta.get("format") != None
            and self.__meta["format"].get("bit_rate") != None
        ):
            return int(self.__meta["format"]["bit_rate"])

    def video_bitrate_sum(self) -> Optional[int]:
        """
        Return the sum of the bitrates of all video streams.
        """
        if isinstance(self.video_bitrates(), int):
            return int(self.video_bitrates())
        elif isinstance(self.video_bitrates(), dict):
            return sum(value for key, value in dict(self.video_bitrates()))


if __name__ == "__main__":
    pass

del Dict, Union, Optional
