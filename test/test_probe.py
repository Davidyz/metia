import os
import unittest
from metia import probe


class TestProbe(unittest.TestCase):
    media_dir = os.path.sep.join(
        __file__.split(os.path.sep)[:-1] + ["media_files"]
    )

    def test_read(self):
        self.assertIsInstance(
            probe.Probe(f"{self.media_dir}/no_audio.mp4"), probe.Probe
        )

    def test_wrong_path(self):
        with self.assertRaises(FileNotFoundError) as exception:
            probe.Probe("asdhfo")

    def test_equal_probe(self):
        self.assertEqual(
            probe.Probe(f"{self.media_dir}/no_audio.mp4"),
            probe.Probe(f"{self.media_dir}/no_audio.mp4"),
        )

    def test_equal_dict(self):
        self.assertEqual(
            probe.Probe(f"{self.media_dir}/no_audio.mp4"),
            probe.Probe(f"{self.media_dir}/no_audio.mp4").dict(),
        )

    def test_empty_audio(self):
        clip = probe.Probe(f"{self.media_dir}/no_audio.mp4")
        self.assertEqual(clip.audio_codec(), {})

    def test_audio_codec(self):
        song = probe.Probe(f"{self.media_dir}/Canon Rock.mp3")
        self.assertEqual(song.audio_codec(), {0: "mp3"})

    def test_video_codec(self):
        clip = probe.Probe(f"{self.media_dir}/no_audio.mp4")
        self.assertEqual(clip.video_codec(), {0: "h264"})

    def test_audio_bitrates(self):
        song = probe.Probe(f"{self.media_dir}/Canon Rock.mp3")
        self.assertEqual(song.audio_bitrates(), {0: 320000})

    def test_video_bitrates(self):
        clip = probe.Probe(f"{self.media_dir}/no_audio.mp4")
        self.assertEqual(clip.video_bitrates(), {0: 27949364})


if __name__ == "__main__":
    unittest.main()
