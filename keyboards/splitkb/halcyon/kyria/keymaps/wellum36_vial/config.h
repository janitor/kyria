#pragma once

#define VIAL_KEYBOARD_UID {0x9A, 0x6E, 0x9C, 0x8D, 0x57, 0x0D, 0x83, 0xEE}
#define VIAL_UNLOCK_COMBO_ROWS {0, 4}
#define VIAL_UNLOCK_COMBO_COLS {1, 1}

#define VIA_EEPROM_LAYOUT_OPTIONS_SIZE 2
#define DYNAMIC_KEYMAP_LAYER_COUNT 8

// Place Wellum's 3x5+3 keys on the same Kyria positions used by Miryoku.
#define LAYOUT_split_3x5_3( \
    L00, L01, L02, L03, L04, R00, R01, R02, R03, R04, \
    L10, L11, L12, L13, L14, R10, R11, R12, R13, R14, \
    L20, L21, L22, L23, L24, R20, R21, R22, R23, R24, \
    LT0, LT1, LT2, RT0, RT1, RT2 \
) \
LAYOUT( \
    KC_NO, L00, L01, L02, L03, L04, R00, R01, R02, R03, R04, KC_NO, \
    KC_NO, L10, L11, L12, L13, L14, R10, R11, R12, R13, R14, KC_NO, \
    KC_NO, L20, L21, L22, L23, L24, KC_NO, KC_NO, KC_NO, KC_NO, R20, R21, R22, R23, R24, KC_NO, \
    KC_NO, LT0, LT1, LT2, KC_NO, KC_NO, RT0, RT1, RT2, KC_NO \
)
