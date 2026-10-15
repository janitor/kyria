# Kyria rev4: Miryoku QWERTY and Wellum 36

This userspace builds QMK firmware for a wired Halcyon Kyria rev4 with the
Halcyon TFT display on the left half and no module on the right half. Miryoku
QWERTY and Wellum 36 are provided, along with a Vial-enabled Wellum 36 variant.
Flash a matching pair of files.

## Wellum 36

`wellum36` follows [Wellum 36](https://github.com/braindefender/wellum/blob/master/for-36-keys_en.md): QWERTY letters, one-shot modifiers, navigation and symbol layers, and a gaming layer. Its three middle thumb keys on each half are:

| Half | Left to right |
| --- | --- |
| Left | Language (Caps Lock), Space, Nav |
| Right | Sym, Shift, Alt |

Wellum 36 is designed for the **Ortho** variant of
[Universal Layout](https://github.com/braindefender/universal-layout) on the
host computer. Install and select that input source before relying on the
Wellum symbols or Russian letters. The Mac's built-in keyboard uses the same
active input source unless you switch it yourself or configure your own
per-device solution.

`wellum36_vial` has the same default layers and custom keycodes as `wellum36`,
but can be edited in Vial after flashing. Vial exposes eight layers. The
one-shot modifiers and window/tab switchers appear in its User tab. Changes
made in Vial are stored on the keyboard and can replace the default mappings;
use Vial's reset action to restore the compiled defaults.
On the left TFT, this variant shows the active layer's number (0–7), name, and two short
hints. It does not show a language indicator. The names follow the eight
compiled Wellum layers; changing their purpose in Vial does not rename them.

The Wellum source copied here is from commit
`2b0fd86a1996b4ce7b4f33e80f9d557120f5258f` of the Wellum repository.
The Kyria mapping and Halcyon module definitions are local adaptations.

## Miryoku QWERTY

The keymap uses Miryoku's QWERTY base and its original generated layer data.
The physical mapping follows Miryoku's Kyria layout: the central five columns
of each half and the middle three keys of each thumb cluster are used. The
other keys are intentionally disabled.

The middle three thumb keys, from left to right on each half, are:

| Half | Tap | Hold |
| --- | --- | --- |
| Left, inner three | Esc, Space, Tab | Media, Nav, Mouse |
| Right, inner three | Enter, Backspace, Delete | Sym, Num, Fun |

Miryoku's home-row modifiers, navigation, number, symbol, function, media,
mouse, and button layers are retained in their original order. The Halcyon TFT
support has been extended to show its existing number glyphs for layers 8 and
9 as well, so all ten Miryoku layers show a number.

## Build

Follow the setup steps in the [splitkb userspace README](README.md) for the
`halcyon-qmk` branch. Use an upstream QMK checkout, point `user.overlay_dir`
at this repository, then run:

```sh
qmk userspace-compile
```

`qmk.json` contains the two targets for each keymap. For a single Miryoku half:

```sh
qmk compile -kb splitkb/halcyon/kyria/rev4 -km miryoku_qwerty -e HLC_TFT_DISPLAY=1 -e TARGET=kyria_rev4_miryoku_qwerty_left_display
qmk compile -kb splitkb/halcyon/kyria/rev4 -km miryoku_qwerty -e HLC_NONE=1 -e TARGET=kyria_rev4_miryoku_qwerty_right_none
```

The build outputs are separate `.uf2` files. Keep the left and right filenames
distinct when flashing.

For Wellum 36, use `-km wellum36` and the `TARGET` names
`kyria_rev4_wellum36_left_display` and `kyria_rev4_wellum36_right_none` with
the same left `HLC_TFT_DISPLAY=1` and right `HLC_NONE=1` options.

### Build Wellum 36 with Vial

Clone [vial-qmk](https://github.com/vial-kb/vial-qmk) with submodules and
configure this userspace as its overlay. Build each half separately:

```sh
qmk compile -kb splitkb/halcyon/kyria/rev4 -km wellum36_vial -e HLC_TFT_DISPLAY=1 -e TARGET=kyria_rev4_wellum36_vial_left_display
qmk compile -kb splitkb/halcyon/kyria/rev4 -km wellum36_vial -e HLC_NONE=1 -e TARGET=kyria_rev4_wellum36_vial_right_none
```

Run these commands from a `vial-qmk` checkout, not upstream QMK. The
`qmk.json` targets above remain for upstream QMK and are intentionally separate
from this Vial build.

## Flash

Download the original left-display and right-no-module firmware from the
[splitkb Firmware Finder](https://splitkb.com/fw) before replacing it. Connect
one half to the computer by USB. Double-tap its controller Reset button to
mount `RPI-RP2`, then copy that half's `.uf2` file to the drive. Repeat with
the other half. Do not disconnect the interconnect cable while either half is
powered. See the [splitkb wired flashing guide](https://docs.splitkb.com/product-guides/halcyon-series/build-guide/wired/firmware).

## Source

The Halcyon hardware and module support comes from splitkb's `halcyon-qmk`
userspace branch (commit `0e44cb2c1c26db8a63d0331ebad85bd8df75bd18`).
The keymap and generated layer headers come from
[Miryoku QMK](https://github.com/manna-harbour/miryoku_qmk), branch `miryoku`
(commit `a014046cc6910aa77dbeca2aa41ca407d5ef1446`). The upstream-QMK UF2
files were built against commit `7a1bbf37c5c07da4ea0a162bb139083a46ef40a1`.
The Vial-enabled Wellum UF2 files were built against vial-qmk commit
`dd43959ae5c08d8a28d38a1acf7b04e86b14a344`.
Both projects use GPL-2.0-or-later compatible terms as indicated in their
source files. This repository retains those notices in the copied files.
