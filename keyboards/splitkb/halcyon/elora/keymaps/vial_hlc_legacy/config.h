// Copyright 2024 splitkb.com (support@splitkb.com)
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

#define VIAL_KEYBOARD_UID {0x91, 0xC0, 0x72, 0xB1, 0xEA, 0x3F, 0xF0, 0xBA}

#define VIAL_UNLOCK_COMBO_ROWS { 0, 6 }
#define VIAL_UNLOCK_COMBO_COLS { 1, 1 }

// Increase the EEPROM size for layout options
#define VIA_EEPROM_LAYOUT_OPTIONS_SIZE 2

#define RGB_MATRIX_FRAMEBUFFER_EFFECTS
#define RGB_MATRIX_KEYPRESSES

#define DYNAMIC_KEYMAP_LAYER_COUNT 8

#define HALCYON_LEGACY

#undef MATRIX_ROWS
#define MATRIX_ROWS 12
#define LAYOUT_elora_hlc(k0G, k0F, k0E, k0D, k0C, k0B, k6B, k6C, k6D, k6E, k6F, k6G, k1G, k1F, k1E, k1D, k1C, k1B, k7B, k7C, k7D, k7E, k7F, k7G, k2G, k2F, k2E, k2D, k2C, k2B, k8B, k8C, k8D, k8E, k8F, k8G, k3G, k3F, k3E, k3D, k3C, k3B, k4D, k3A, k9A, k10D, k9B, k9C, k9D, k9E, k9F, k9G, k4E, k4C, k4B, k4F, k4A, k10A, k10F, k10B, k10C, k10E, k5A, k5B, k5C, k5D, k5E, k11A, k11B, k11C, k11D, k11E) { \
    {KC_NO, k0B, k0C, k0D, k0E, k0F, k0G}, \
    {KC_NO, k1B, k1C, k1D, k1E, k1F, k1G}, \
    {KC_NO, k2B, k2C, k2D, k2E, k2F, k2G}, \
    {k3A, k3B, k3C, k3D, k3E, k3F, k3G}, \
    {k4A, k4B, k4C, k4D, k4E, k4F, KC_NO}, \
    {k5A, k5B, k5C, k5D, k5E, KC_NO, KC_NO}, \
    {KC_NO, k6B, k6C, k6D, k6E, k6F, k6G}, \
    {KC_NO, k7B, k7C, k7D, k7E, k7F, k7G}, \
    {KC_NO, k8B, k8C, k8D, k8E, k8F, k8G}, \
    {k9A, k9B, k9C, k9D, k9E, k9F, k9G}, \
    {k10A, k10B, k10C, k10D, k10E, k10F, KC_NO}, \
    {k11A, k11B, k11C, k11D, k11E, KC_NO, KC_NO} \
}
