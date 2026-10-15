# Wireless Kyria keymap cheat sheet

For the Halcyon Kyria rev4 with a USB-C dongle, the Wellum 36 QWERTY firmware keymap, and Universal Layout Ortho on macOS. This describes the current firmware defaults, including changes copied from ZMK Studio. Later Studio edits may override these defaults.

## BASE layer

Keys are shown left to right. Letters and symbols are shown as **English / Russian** output with Universal Layout Ortho selected. `·` marks an unused position.

```text
Left half                              Right half
Tab  q/й  w/ц  e/у  r/к  t/е          y/н  u/г  i/ш  o/з  p/х  BkSp
Esc  a/ф  s/ы  d/в  f/а  g/п          h/р  j/о  k/л  l/д  ~/ж   ·
·    z/я  x/ч  c/с  v/м  b/и  F13    n/т  m/ь  &/б  [/ю  ]/э   ·

Left thumb keys             Right thumb keys
LCmd  Caps  Space  NAV  ALT   Caps  SYM  Shift  ALT  RCmd
```

Hold a thumb key to activate its layer; release it to return to BASE. `ALT` is available on both halves: the rightmost left thumb key and the second rightmost right thumb key.

## Common actions

| Action | Keys |
| --- | --- |
| Backspace | Extra key right of `P` on BASE, SYM, and NUM; or `NAV` + `O` |
| Tab / Escape | Outer top and middle keys on the left |
| Forward Delete | `NAV` + `P` |
| Enter | `NAV` + `G` or `NAV` + `H` |
| Escape | `NAV` + `T` or `NAV` + `Y` |
| Arrow keys ← ↓ ↑ → | `NAV` + `J` / `K` / `L` / `;` |
| Home / End | `NAV` + `U` / `I` |
| Page Up / Down | `NAV` + `M` / `,` |
| Digits `1`–`5` | Hold `NAV` + `SYM`, then press `Q` / `W` / `E` / `R` / `T` |
| Digits `6`–`0` | Hold `NAV` + `SYM`, then press `Y` / `U` / `I` / `O` / `P` |
| Symbols `! @ # $ %` | `SYM` + `Q` / `W` / `E` / `R` / `T` |
| Symbols `^ ? * ( )` | `SYM` + `Y` / `U` / `I` / `O` / `P` |
| F1–F5 | `SYM` + `NAV` + `Z` / `X` / `C` / `V` / `B` |
| F6–F10 | `SYM` + `NAV` + `N` / `M` / `,` / `.` / `/` |
| F11 / F12 | `SYM` + `NAV` + `G` / `H` |
| Select Universal Layout Ortho | Extra `F13` key next to `B`; Karabiner selects this input source |
| Switch English / Russian | `Caps`, the second left thumb key; verified on Kyria |
| Next window of current Mac app | `NAV` + `W` sends Command + Grave |
| Next / previous tab | `NAV` + `Q` or `R` sends Control + Tab; `NAV` + `E` sends Control + Shift + Tab |

Holding `SYM` and `NAV` together activates `NUM`. Its top row sends keypad digits and its lower letter row sends F1–F10. `SYM` alone sends symbols under Universal Layout Ortho.

On `SYM`, the left top row `Q W E R T` produces `! @ # $ %`; `A S D F G` produces `~/ж`, Grave, apostrophe, quotation mark, and `-`; `Z X C V B` produces backslash, `¦ ; , _`. On the right, `Y U I O P` produces `^ ? * ( )`; `H J K L ;` produces `+` and sticky modifiers; `N M , . /` produces `= . : | /`. `⇧ ⌃ ⌥ ⌘` are sticky Shift, Control, Option, and Command. `~/ж` depends on Caps state.

## Language and Mac shortcuts

With Universal Layout Ortho selected in macOS, press the second left thumb key (`Caps`) to switch between English and Russian within that layout. The macOS input source remains the same. Polish is a separate input source.

Karabiner rules also let left Command select U.S., right Command select Russian, and both Command keys select Polish. The extra `F13` key next to `B` returns to Universal Layout Ortho.

On `NAV`, `Q` and `R` send Control + Tab; `E` sends Control + Shift + Tab. These switch tabs in apps that support the shortcuts. `NAV` + `W` sends Command + Grave for the next window of the current app. For app switching, `NAV` + `A` applies sticky Command, then `NAV` + `B` or `NAV` + `N` sends Tab. This sequence follows from the ZMK configuration but has not been physically verified.

## Other layers

- **NAV:** `A S D F` apply sticky Command, Option, Control, and Shift to the next key. `G` is Enter. The right half has another Enter and arrow keys.
- **CMD:** Hold `NAV`, then the key at the `Caps` position. The right top row controls volume; the middle row controls media. While holding both thumb keys, press the extra top-left key next to `Q` to unlock ZMK Studio.
- **ALT:** Hold the rightmost left thumb key or the second rightmost right thumb key. Letter keys send Right Alt with that letter. In Universal Layout Ortho, `ALT` + `T`, `I`, and `M` produce `ё`, `щ`, and `ъ`; `ALT` + `L` and `;` produce `«` and `»`.
- **GAME:** Press `NAV` + `C` to switch to GAME. To return to BASE, press the second left thumb key on the right half (the BASE `SYM` position). On GAME, hold the BASE `NAV` position to activate GFN. The first two left thumb keys then become Escape and Enter.

## ZMK Studio

Connect to the USB-C dongle with [ZMK Studio](https://zmk.studio/) and click **Save** after editing. Its ordinary Backspace is **Key Press → Keyboard Delete**. **Keypad Backspace** is a different keycode; **Keyboard Delete Forward** deletes to the right of the cursor. Studio changes persist on the dongle and can override firmware defaults.

Firmware keymap: [`config/halcyon_kyria.keymap`](config/halcyon_kyria.keymap).
