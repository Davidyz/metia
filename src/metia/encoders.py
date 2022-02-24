from . import utils


FLAC = "flac"
MP3 = "libmp3lame" if "libmp3lame" in utils.get_encoders() else "mp3"

if __name__ == "__main__":
    pass
