# Saved ZMK Studio keymap

This is a read-only snapshot of the Halcyon Kyria dongle taken over USB before
the settings reset recommended by splitkb support. Studio reported no unsaved
changes. `keymap.pb` is the exact keymap response from the device; `keymap.json`
is a readable decoding of that response plus the selected physical layout.

The device had eight layers with 60 bindings each. Physical layout index 1,
the 60-position Halcyon Kyria layout, was selected. It matches the firmware's
default `zmk,physical-layout`.

Compared with the previously built stock keymap, four bindings differed:

| Layer | Position | Saved binding | Previous stock binding |
| --- | ---: | --- | --- |
| BASE | 44 | `&mo ALT` | `&kp LALT` |
| BASE | 45 | `&kp CAPS` | `&none` |
| SYM | 11 | `&kp BSPC` | `&none` |
| NUM | 11 | `&kp BSPC` | `&none` |

These bindings are now incorporated into `../../config/halcyon_kyria.keymap`.
The snapshot contains keymap bindings, layer names, and the selected physical
layout. It does not contain Bluetooth bonding keys or other persistent device
settings.
