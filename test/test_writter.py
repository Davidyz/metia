import os
import unittest

import metia


class TestWritter(unittest.TestCase):
    media_dir = os.path.sep.join(
        __file__.split(os.path.sep)[:-1] + ["media_files"]
    )
    original_file = f"{media_dir}/Canon Rock.mp3"
    no_meta_file = f"{media_dir}/blank.mp3"

    def setUp(self):
        os.system(
            f'ffmpeg -hide_banner -loglevel quiet -y -i "{self.original_file}" -map_metadata -1 -map 0 -c copy {self.no_meta_file}'
        )

    def tearDown(self):
        if os.path.isfile(self.no_meta_file):
            os.system(f"rm {self.no_meta_file}")

    def test_get_probe(self):
        self.assertEqual(
            metia.probe.Probe(self.original_file),
            metia.writter.Media(self.original_file).probe(),
        )

    def test_create_from_probe(self):
        self.assertEqual(
            metia.writter.Media(self.original_file),
            metia.writter.Media(metia.probe.Probe(self.original_file)),
        )

    def test_path(self):
        self.assertEqual(
            os.path.realpath(metia.writter.Media(self.original_file).path),
            os.path.realpath(self.original_file),
        )

    def test_get_tags(self):
        self.assertEqual(
            metia.probe.Probe(self.original_file).get_tags(),
            metia.writter.Media(self.original_file).get_tags(),
        )

    def test_tag_io(self):
        new_song = metia.writter.Media(self.no_meta_file)
        new_song.set_tag("title", "Canon Rock")
        new_song.write_song_tags()

        new_probe = metia.probe.Probe(self.original_file)
        self.assertIsInstance(new_probe.get_tags(), dict)
        if isinstance(new_probe.get_tags(), dict):
            self.assertEqual(new_probe.get_tag("title"), "Canon Rock")


if __name__ == "__main__":
    unittest.main()
