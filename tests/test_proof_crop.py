import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import fitz
from PIL import Image


SCRIPT = (Path(__file__).resolve().parents[1] / "skills" / "task-first-manual" /
          "scripts" / "proof_crop.py")


class CropProofTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.source = Path(temp.name) / "source.pdf"
        self.output = Path(temp.name) / "proof.png"
        with fitz.open() as doc:
            page = doc.new_page(width=300, height=450)
            for y, state in ((90, "Saved"), (320, "Save failed")):
                page.insert_text((60, y), state)
                page.insert_text((60, y + 20), "Close")
            page.set_rotation(90)
            doc.save(self.source)

    def run_crop(self, box, phrase):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.source), "--page", "1",
             "--box", *map(str, box), "--expect", phrase, "--out", str(self.output)],
            capture_output=True, text=True,
        )

    def test_correct_panel_on_rotated_page(self):
        before = self.source.read_bytes()
        result = self.run_crop((40, 50, 180, 130), "Saved")
        self.assertEqual(result.returncode, 0, result.stderr)
        with Image.open(self.output) as proof:
            self.assertEqual(proof.format, "PNG")
            self.assertIsNotNone(proof.convert("L").point(lambda v: 255 if v < 100 else 0).getbbox())
        self.assertEqual(self.source.read_bytes(), before)

    def test_empty_or_ambiguous_region(self):
        for box, phrase in [((40, 285, 180, 360), "Saved"),
                            ((40, 50, 180, 360), "Close")]:
            with self.subTest(phrase=phrase):
                self.assertNotEqual(self.run_crop(box, phrase).returncode, 0)
                self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
