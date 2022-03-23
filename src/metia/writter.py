import os
import uuid
import shutil
from typing import Dict, Optional, Union

from . import probe

FFMPEG_COMMAND = "ffmpeg"


class Media:
    __SONG_TAGS = {"album", "artist", "title"}

    def __init__(self, media: Union[probe.Probe, str]):
        if isinstance(media, str):
            if os.path.isfile(media):
                self.__probe: probe.Probe = probe.Probe(media)
            else:
                raise FileNotFoundError(f"{media} is not found.")
        elif isinstance(media, probe.Probe):
            self.__probe: probe.Probe = probe.Probe(media.path)
        elif not isinstance(media, (probe.Probe, str)):
            raise TypeError(
                "media has to be one of the following types: str, probe.Probe."
            )
        self.__cover: Optional[str] = None
        self.__tags: Dict[str, str] = (
            self.get_tags() if not (self.get_tags() is None) else {}
        )
        self.__filename = self.__probe.path.split(os.path.sep)[-1]
        self.__suffix = self.__filename.split(".")[-1]

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, (Media, probe.Probe)) and self.path == other.path
        )

    @property
    def path(self) -> str:
        return self.__probe.path

    def probe(self) -> probe.Probe:
        return self.__probe

    def find_song_cover(self, path: Optional[str] = None) -> bool:
        """
        Try to set the cover image.
        If an argument is not provided, it tries to find cover.jpg from the same directory.
        Return True if image is set.
        """
        if isinstance(self.__cover, str) and os.path.isfile(self.__cover):
            # cover is already found
            return True
        elif any(
            self.__probe.video_codec()[i] == "mpeg"
            for i in self.__probe.video_codec().keys()
        ):
            # the file already has a cover art
            return True
        elif (
            isinstance(path, str)
            and path.endswith(".jpg")
            and os.path.isfile(path)
        ):
            self.__cover = path
            return True
        cover_names = ["cover.jpg", "Cover.jpg"]
        song_dir = os.path.sep.join(self.__probe.path.split(os.path.sep)[:-1])
        if path is None:
            # trying to find the cover from the same directory
            for name in cover_names:
                existing_cover_path = os.path.join(song_dir, name)
                if os.path.isfile(existing_cover_path):
                    self.__cover = existing_cover_path
                    return True
            return False
        elif not os.path.isfile(path):
            raise FileNotFoundError(f"{path} is not a file.")

        path = os.path.expanduser(str(path))

        try:
            probe.Probe(path)
            shutil.copy(path, song_dir)
        except Exception as e:
            if not isinstance(e, shutil.SameFileError):
                return False

        return isinstance(self.__cover, str)

    def get_tags(self) -> Dict[str, str]:
        return self.__probe.get_tags() or {}

    def get_tag(self, key: str) -> Optional[str]:
        return self.__probe.get_tag(key)

    def set_tag(self, key: str, value: str, encoding="utf8") -> None:
        self.__tags[key.upper() if key in self.__SONG_TAGS else key] = value

    def set_song_cover(self):
        """
        Embed the album art into the media.
        This requires a self.__cover to be set to an image. If not, a FileNotFoundError will be thrown.
        """
        if not self.find_song_cover():
            raise FileNotFoundError(
                "Failed to find a cover art in the directory of the media."
            )
        elif any(
            self.__probe.video_codec()[i] == "mjpeg"
            for i in self.__probe.video_codec().keys()
        ):
            # the file already has a cover art
            return
        random_name = str(uuid.uuid4()) + "." + self.__suffix
        while random_name in os.listdir():
            random_name = str(uuid.uuid4()) + "." + self.__suffix
        command = f'{FFMPEG_COMMAND} -i "{self.__probe.path}" -i "{self.__cover}" -loglevel 0 -hide_banner -map 0:0 -map 1:0 -c copy -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" -disposition:v attached_pic {random_name}'
        if os.system(command) == 0:
            shutil.move(random_name, self.path)
            self.__probe._init()

    def write_song_tags(self):
        command = f'{FFMPEG_COMMAND} -hide_banner -loglevel 0 -i "{self.path}" -map 0 -c copy'
        for key in self.__SONG_TAGS:
            value = self.get_tags().get(key.upper())
            if isinstance(value, str):
                command += " -metadata {key}={value} ".format(
                    key=key, value=value.replace(" ", "\\ ")
                )

        random_name = str(uuid.uuid4()) + "." + self.__suffix
        while random_name in os.listdir():
            random_name = str(uuid.uuid4()) + "." + self.__suffix

        command += f" {random_name}"
        if os.system(command) == 0:
            shutil.move(random_name, self.path)
            self.__probe._init()


if __name__ == "__main__":
    pass
