# Wireless Kyria rev4 firmware

This configuration is for a splitkb Halcyon Kyria rev4 with two Halcyon
Wireless Controllers, CR1632 coin-cell battery boards, no display or other
Halcyon modules, and the Halcyon USB-C dongle. It uses ZMK, not the wired QMK
firmware in the parent directory.

## Firmware revisions used for the latest build

The regular images built on 2026-10-13 after the support-requested settings
reset use these pinned upstream revisions:

| Component | Repository | Commit |
| --- | --- | --- |
| ZMK firmware | [splitkb/zmk](https://github.com/splitkb/zmk) | [`f0821fb5e7f1577bcfce36fb4ce899cfb395f00a`](https://github.com/splitkb/zmk/commit/f0821fb5e7f1577bcfce36fb4ce899cfb395f00a) |
| Halcyon hardware module | [splitkb/zmk-halcyon-module](https://github.com/splitkb/zmk-halcyon-module) | [`a83eaa492a678ed12fb5feabc62426dc1ed3a3cb`](https://github.com/splitkb/zmk-halcyon-module/commit/a83eaa492a678ed12fb5feabc62426dc1ed3a3cb) |

The exact build manifest is [`config/west.yml`](config/west.yml). All three
regular build targets below use that manifest; [`build.yaml`](build.yaml)
lists their boards and shields. The local build uses the
`zmkfirmware/zmk-dev-arm:4.1-branch` Docker image. The SHA-256 hashes of the
three locally built UF2 files are recorded in
[`firmware/SHA256SUMS`](firmware/SHA256SUMS). The UF2 binaries themselves are
excluded from Git.

I reported flashing settings-reset firmware and then newly built regular
images to both halves and the dongle on 2026-10-13. The firmware has not been
read back from the devices, so the repository records the build inputs and
local output hashes rather than independently verifying the installed bytes.
An earlier right-half diagnostic build is documented separately in
[`firmware/diagnostic-right-2026-10-13/`](firmware/diagnostic-right-2026-10-13/);
it is not the latest three-device build.

`build.yaml` defines three distinct images:

| Image | Hardware | Role |
| --- | --- | --- |
| `kyria-dongle-wellum36.uf2` | Halcyon USB-C dongle | Central, USB output, keymap, ZMK Studio |
| `kyria-left-coincell.uf2` | Left Halcyon Wireless Controller and coin cell | Wireless peripheral |
| `kyria-right-coincell.uf2` | Right Halcyon Wireless Controller and coin cell | Wireless peripheral |

The eight-layer Wellum 36 QWERTY map originated from
`../keyboards/splitkb/halcyon/kyria/keymaps/wellum36_vial/keymap.c` and now
includes the user's ZMK Studio edits. On `BASE`, the outer top keys are Tab
and Backspace, the outer middle-left key is Escape, and the key next to B
sends F13 for the macOS Karabiner layout switch. The outer thumb keys send
left and right GUI. The rightmost left thumb key activates `ALT`, and the
leftmost right thumb key sends Caps Lock. `SYM` + `NAV`
activates `NUM`; `NAV` reaches `CMD` and switches to `GAME`; `GAME` reaches
`GFN` and can switch back to `BASE`. On `CMD`, the outermost upper-left key
unlocks ZMK Studio. Reach it by holding `NAV`, holding the thumb key at the
Caps Lock position (`CMD` on `NAV`), then pressing the outermost key at the
upper-left corner.

The original QMK one-shot modifiers had no expiry. ZMK sticky keys in this
configuration expire after 60 seconds of inactivity and release when the next
key is pressed. QMK also cancelled a queued modifier on `SYM` or `NAV`, while
ZMK may carry it to the next ordinary key. On macOS, `NAV` + `W` sends
Command+Grave for the next window of the current app. The Ctrl+Tab browser
switcher sends Ctrl+Tab per press. The `GFN` reset and
bootloader bindings address the dongle, because it is the central controller;
use each half's physical reset control when flashing that half. These are the
main behavior differences.

Changes made only in Vial's persistent storage are not copied here. ZMK Studio
changes are stored on the dongle and persist through normal firmware updates;
the keymap in this repository is the stock layout used after a Studio settings
reset. Port future Studio edits into this file before rebuilding if the stock
layout should include them. The `west.yml` manifest
pins the splitkb ZMK fork and Halcyon module to known commits. Run
`./build-local.sh` from this directory to rebuild all three images with Docker;
it places the results and their SHA-256 checksums in `firmware/`.

The firmware files are preparation artifacts. Copying them to the hardware is
a separate step.

This directory contains a custom keymap and pinned upstream revisions, but no
local changes to the ZMK or Halcyon module source code. The firmware binaries
are generated locally and excluded from Git. The keymap runs on the dongle;
the left and right controllers are wireless peripherals. The macOS layout and
Karabiner rules in `../macos-layout/` run on the host computer.

On 2026-10-13, the right half was flashed with a firmware build that disables
the unused NC-pin scanner when no encoder is installed. The right controller
was reset once after flashing, and both halves typed through the dongle.
Battery life with that build was not established.

Later that day, splitkb added low-duty BLE advertising for coin-cell
peripherals when their connection is lost. `config/west.yml` now pins the
matching ZMK and Halcyon module commits, and all three UF2 files were rebuilt.
Both `left` and `right` builds have
`CONFIG_ZMK_BLE_LOW_DUTY_ADVERTISING=y`, as well as battery-mode RGB and
external-power shutdown. The dongle keymap was then synchronized with the
current saved ZMK Studio layout. Its eight layers contain 480 bindings; the
four differences from the previous source were added to `config/halcyon_kyria.keymap`.
The full read-only snapshot is in `backups/studio-2026-10-13/`.

Splitkb support recommended flashing `settings_reset` on both halves and the
dongle, followed by the corresponding regular image on each device. The reset
images are in `firmware/reset/`. This clears stored pairings and Studio
settings; the keymap in `config/` contains the previously copied Studio edits.
The active 60-position physical layout is already the firmware default.
On 2026-10-13, all three devices were flashed with the settings-reset images
and then with newly built regular firmware. Both halves worked afterward.
By 2026-10-15, the right half had drained a third CR1632 within seven days;
the left half continued to work normally. The keyboard appeared to sleep when
idle because it took a moment to respond after a period of inactivity. This
is an observation, not a measured power-consumption result.

After flashing a regular image to each wireless controller, press its Reset
button once, as required by the splitkb wireless guide.

## Keymap cheat sheet

`CHEATSHEET.md` and `CHEATSHEET.pdf` describe the same firmware keymap in
English. Russian characters in the key diagrams are output data. To regenerate
the PDF, install ReportLab and fontconfig, then run
`python3 generate_cheatsheet.py`. Set `KYRIA_FONT_DIR` to a directory containing
`NotoSans-Regular.ttf`, `NotoSans-Bold.ttf`, and `DejaVuSans-Bold.ttf` for full
symbol coverage; otherwise the script uses fonts found by `fc-match`.
