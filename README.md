# Metia

A tool (and a wrapper of [FFmpeg][ffmpeg_url]) to manipulate metadata of audio
files.

This library is developed under Python 3.8.

## Installation

```bash
pip install metia
```

## Dependency

[FFmpeg][ffmpeg_url]

## Usage

All of the functionalities requires a ffmpeg/ffprobe build that has the
corresponding codec that the media is using. To set a custom build of
`ffmpeg`/`ffprobe`, set the variables `metia.probe.FFPROBE_COMMAND` and/or
`metia.writter.FFMPEG_COMMAND`.

### `metia.probe.Probe`

If all you want to do is to read the metadata, use this class. This provides a
wrapper of `ffprobe` to extract commonly-used media metadata, such as bit-rate
and codec.

Some methods of this class may be helpful to video files too.

### `metia.writter.Media`

> > WORK IN PROGRESS

This class, apart from reading the metadata, allows you to alter the metadata,
including changing the tags of the media file and adding a cover art to it.

This class, unlike `metia.probe.Probe`, is highly targeted to music files (with
or without cover art). Although it is possible to integrate some video-related
features, the demands might differ so much that it's unworthy compared to using
the original `ffmpeg` commands. Thus, I believe a better way to utilize this
library with videos is to use `metia.probe.Probe` to extract the information you
want and use `os.system` (or other equivalent) to invoke a `ffmpeg` command.
Alternatively, you may look for other more powerful ffmpeg wrappers that has
support for more ffmpeg features, but that is beyond the scope of this project.

### Command Line Interface

This tool provides command-line interface for convenience.

- `metia-probe`: print the media info in a nicer (less messy) format

## Development

This library is hosted on this [Github repository][repo_url]. Visit to fork or
create issue/PR.

[ffmpeg_url]: https://www.ffmpeg.org/
[repo_url]: https://github.com/Davidyz/metia
