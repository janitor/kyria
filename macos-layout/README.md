# Universal Ortho Split for macOS

This directory contains separate English and Russian versions of the installed
Universal Layout Ortho. The split bundle is installed in
`~/Library/Keyboard Layouts/Universal Ortho Split.bundle`. The original
`Universal.bundle` and Kyria firmware are unchanged.

Both sources are enabled in macOS. The replacement Karabiner rule is active in
the default profile, and a copy is stored at
`~/.config/karabiner/assets/complex_modifications/kyria-universal-ortho-split.json`.
The previous Karabiner configuration is backed up at
`~/.config/karabiner/karabiner.before-ortho-split-enable.20261011-123111.json`.

## Prepared files

- `dist/Universal Ortho Split.bundle` contains two macOS input sources:
  `Universal Ortho EN` and `Universal Ortho RU`. Their menu icons display
  distinct EN and RU labels.
- `karabiner-rule.json` is a replacement for the current rule named
  `Change input source to En by left_command; Ru by right_command; Pl by both commands; Universal by Kyria F13.`
  It retains the three Command shortcuts. On the Kyria dongle, Caps Lock
  switches between the new EN and RU sources; from any other source it selects
  EN. F13 also selects EN. The Caps Lock and F13 changes apply only to the
  Halcyon Kyria USB dongle (vendor 7504, product 24926).
- macOS reports the source IDs as
  `local.raman.keyboardlayout.universalorthosplit.keylayout.UniversalOrthoEN`
  and `local.raman.keyboardlayout.universalorthosplit.keylayout.UniversalOrthoRU`.
- `source/Universal Layout Ortho.keylayout` is a copy of the currently
  installed layout, SHA-256
  `e00e6001c25c48461e8f7288756ac58c287427926c3abc0e7e7d8d690ad25a06`.
  The upstream project is [braindefender/universal-layout](https://github.com/braindefender/universal-layout).

The builder copies the source's unshifted English and Russian key maps into
separate files. It leaves their shifted keys, shared Option and shortcut
maps, actions, and dead-key terminators intact. Caps Lock is neutralized
inside both layouts so it cannot silently change the language; Karabiner
handles the physical Caps Lock key from the Kyria instead.

## Check the installed setup

1. Press Caps Lock on Kyria to switch between `Universal Ortho EN` and
   `Universal Ortho RU`. The input menu should display distinct EN and RU icons.
2. Kyria F13 selects EN. Left Command still selects the existing U.S. source,
   right Command selects the existing Russian source, and both Commands select
   Polish when that source is available.

Both split sources were selected successfully through the macOS text input
API, and the original source was restored afterward. Physical Kyria key presses
still need a manual check.

The Karabiner rule uses the runtime IDs observed after registration. If a future
macOS version assigns different IDs, inspect Karabiner-EventViewer → Variables
and update the rule patterns.

No Kyria firmware update is needed. The keyboard already sends Caps Lock and
F13, and the new switching happens on the Mac.

## Rebuild and validation

The builder needs Python 3, Pillow, and macOS `iconutil`:

```sh
python3 build_split.py
python3 -m unittest discover -s tests -v
karabiner_cli --lint-complex-modifications karabiner-rule.json
```
