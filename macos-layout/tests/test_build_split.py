import json
import plistlib
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "Universal Layout Ortho.keylayout"
SCRIPT = ROOT / "build_split.py"


def key_map(xml: str, map_set: str, index: int) -> str:
    group = re.search(
        rf'<keyMapSet id="{map_set}">(.*?)</keyMapSet>', xml, re.S
    )
    if group is None:
        raise AssertionError(f"Missing key map set {map_set}")
    match = re.search(
        rf'<keyMap index="{index}"[^>]*>(.*?)</keyMap>', group.group(1), re.S
    )
    if match is None:
        raise AssertionError(f"Missing key map {index} in {map_set}")
    return match.group(1)


class SplitLayoutBuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.result = subprocess.run(
            [sys.executable, str(SCRIPT), "--source", str(SOURCE),
             "--output-dir", cls.temp.name],
            text=True, capture_output=True,
        )
        cls.bundle = Path(cls.temp.name) / "Universal Ortho Split.bundle"
        cls.original = SOURCE.read_text(encoding="utf-8") if SOURCE.exists() else ""

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_languages_preserve_original_ortho_maps(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)
        resources = self.bundle / "Contents" / "Resources"
        for name, original_base in (("EN", 0), ("RU", 2)):
            generated = (resources / f"Universal Ortho {name}.keylayout").read_text(
                encoding="utf-8"
            )
            self.assertIn(f'name="Universal Ortho {name}"', generated)
            for index in range(4):
                expected = original_base + index % 2
                self.assertEqual(
                    key_map(generated, "16c", index),
                    key_map(self.original, "16c", expected),
                    (name, index),
                )
            for index in range(4, 8):
                self.assertEqual(
                    key_map(generated, "16c", index),
                    key_map(self.original, "16c", index),
                    (name, index),
                )
            for index in range(8):
                self.assertEqual(
                    key_map(generated, "994", index),
                    key_map(self.original, "994", index),
                    (name, "994", index),
                )
            self.assertEqual(
                re.search(r'<modifierMap\b.*?</modifierMap>', generated, re.S).group(),
                re.search(r'<modifierMap\b.*?</modifierMap>', self.original, re.S).group(),
            )
            for section in ("actions", "terminators"):
                pattern = rf'<{section}>(.*?)</{section}>'
                self.assertEqual(
                    re.search(pattern, generated, re.S).group(1),
                    re.search(pattern, self.original, re.S).group(1),
                    (name, section),
                )
            self.assertTrue((resources / f"Universal Ortho {name}.icns").read_bytes().startswith(b"icns"))

    def test_normal_and_shifted_letters_are_fixed_to_the_selected_language(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)
        resources = self.bundle / "Contents" / "Resources"
        expected = {
            "EN": ("a", "A", "q", "Q"),
            "RU": ("ф", "Ф", "й", "Й"),
        }
        for label, (a, shifted_a, q, shifted_q) in expected.items():
            generated = (resources / f"Universal Ortho {label}.keylayout").read_text(
                encoding="utf-8"
            )
            for index, first, twelfth in ((0, a, q), (1, shifted_a, shifted_q),
                                          (2, a, q), (3, shifted_a, shifted_q)):
                mapping = key_map(generated, "16c", index)
                self.assertIn(f'<key code="0" output="{first}"/>', mapping)
                self.assertIn(f'<key code="12" output="{twelfth}"/>', mapping)

    def test_bundle_exposes_two_distinct_system_sources(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)
        with (self.bundle / "Contents" / "Info.plist").open("rb") as stream:
            info = plistlib.load(stream)
        en = info["KLInfo_Universal Ortho EN"]
        ru = info["KLInfo_Universal Ortho RU"]
        self.assertEqual(en["TISIntendedLanguage"], "en")
        self.assertEqual(ru["TISIntendedLanguage"], "ru")
        self.assertEqual(
            en["TISInputSourceID"],
            "local.raman.keyboardlayout.universalorthosplit.keylayout.UniversalOrthoEN",
        )
        self.assertEqual(
            ru["TISInputSourceID"],
            "local.raman.keyboardlayout.universalorthosplit.keylayout.UniversalOrthoRU",
        )
        self.assertNotEqual(en["TISInputSourceID"], ru["TISInputSourceID"])
        self.assertFalse(en["TICapsLockLanguageSwitchCapable"])
        self.assertFalse(ru["TICapsLockLanguageSwitchCapable"])

    def test_karabiner_rule_is_scoped_to_kyria_and_toggles_split_sources(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)
        with (ROOT / "karabiner-rule.json").open() as stream:
            rule = json.load(stream)
        manipulators = rule["rules"][0]["manipulators"]
        caps = [item for item in manipulators
                if item["from"].get("key_code") == "caps_lock"]
        f13 = [item for item in manipulators
               if item["from"].get("key_code") == "f13"]
        self.assertEqual(len(caps), 2)
        self.assertEqual(len(f13), 1)
        self.assertTrue(any(item["from"].get("key_code") == "left_command"
                            for item in manipulators))
        self.assertTrue(any(item["from"].get("key_code") == "right_command"
                            for item in manipulators))
        for item in caps + f13:
            self.assertTrue(any(condition["type"] == "device_if"
                                for condition in item["conditions"]))
        self.assertTrue(any(condition["type"] == "input_source_if"
                            for condition in caps[0]["conditions"]))
        self.assertTrue(any(condition["type"] == "input_source_unless"
                            for condition in caps[1]["conditions"]))
        with (self.bundle / "Contents" / "Info.plist").open("rb") as stream:
            info = plistlib.load(stream)
        en_id = info["KLInfo_Universal Ortho EN"]["TISInputSourceID"]
        ru_id = info["KLInfo_Universal Ortho RU"]["TISInputSourceID"]
        self.assertTrue(re.fullmatch(
            caps[0]["conditions"][1]["input_sources"][0]["input_source_id"], en_id
        ))
        self.assertTrue(re.fullmatch(
            caps[0]["to"][0]["select_input_source"]["input_source_id"], ru_id
        ))
        self.assertTrue(re.fullmatch(
            caps[1]["to"][0]["select_input_source"]["input_source_id"], en_id
        ))
        self.assertTrue(re.fullmatch(
            f13[0]["to"][0]["select_input_source"]["input_source_id"], en_id
        ))


if __name__ == "__main__":
    unittest.main()
