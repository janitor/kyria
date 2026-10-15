#pragma once

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
