import subprocess
import re
from . import writter


def get_decoders():
    command = f"{writter.FFMPEG_COMMAND} -hide_banner -decoders"
    output = (
        subprocess.run(command.split(" "), capture_output=True)
        .stdout.decode()
        .strip()
        .split("\n")
    )

    pattern = re.compile(r"\s......\s(\w+)\s*.*")
    for i in output:
        match_result = pattern.match(i)
        if match_result is None:
            continue
        yield match_result.groups()[0]


def get_encoders():
    command = f"{writter.FFMPEG_COMMAND} -hide_banner -encoders"
    output = (
        subprocess.run(command.split(" "), capture_output=True)
        .stdout.decode()
        .strip()
        .split("\n")
    )

    pattern = re.compile(r"\s......\s(\w+)\s*.*")
    for i in output:
        match_result = pattern.match(i)
        if match_result is None:
            continue
        yield match_result.groups()[0]


if __name__ == "__main__":
    pass
