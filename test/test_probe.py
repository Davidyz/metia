import unittest
import sys

sys.path.append("./src")

from metia import probe


class TestProbe(unittest.TestCase):
    def test_read(self):
        self.assertIsInstance(
            probe.Probe("./test/media_files/no_audio.mp4"), probe.Probe
        )

    def test_wrong_path(self):
        with self.assertRaises(FileNotFoundError) as exception:
            probe.Probe("asdhfo")

    def test_equal_probe(self):
        self.assertEqual(
            probe.Probe("./test/media_files/no_audio.mp4"),
            probe.Probe("./test/media_files/no_audio.mp4"),
        )

    def test_equal_dict(self):
        self.assertEqual(
            probe.Probe("./test/media_files/no_audio.mp4"),
            probe.Probe("./test/media_files/no_audio.mp4").dict(),
        )

    def test_empty_audio(self):
        clip = probe.Probe("./test/media_files/no_audio.mp4")
        self.assertEqual(clip.audio_codec(), {})

    def test_audio_codec(self):
        pass

    def test_video_codec(self):
        clip = probe.Probe("./test/media_files/no_audio.mp4")
        self.assertEqual(clip.video_codec(), {0: "h264"})

    def test_audio_bitrate(self):
        pass

    def test_video_bitrate(self):
        clip = probe.Probe("./test/media_files/no_audio.mp4")
        self.assertEqual(clip.video_bitrate(), {0: 27949364})


if __name__ == "__main__":
    unittest.main()
