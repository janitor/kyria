/* SPDX-License-Identifier: GPL-2.0-or-later */
/* Copyright 2024 splitkb.com <support@splitkb.com> */

#pragma once

#define VIAL_KEYBOARD_UID {0xF8, 0x7A, 0x1D, 0x23, 0x53, 0x9B, 0x54, 0xB9}

#define VIAL_UNLOCK_COMBO_ROWS { 0, 5 }
#define VIAL_UNLOCK_COMBO_COLS { 5, 5 }

#define RGB_MATRIX_FRAMEBUFFER_EFFECTS
#define RGB_MATRIX_KEYPRESSES

#define DYNAMIC_KEYMAP_LAYER_COUNT 8

#define HALCYON_LEGACY

#undef MATRIX_ROWS
#define MATRIX_ROWS 10
#define LAYOUT_corne_hlc(k0A, k0B, k0C, k0D, k0E, k0F, k5F, k5E, k5D, k5C, k5B, k5A, k1A, k1B, k1C, k1D, k1E, k1F, k6F, k6E, k6D, k6C, k6B, k6A, k2A, k2B, k2C, k2D, k2E, k2F, k7F, k7E, k7D, k7C, k7B, k7A, k3D, k3E, k3F, k8F, k8E, k8D, k4A, k4B, k4C, k4D, k4E, k9A, k9B, k9C, k9D, k9E) { \
    {k0A, k0B, k0C, k0D, k0E, k0F}, \
    {k1A, k1B, k1C, k1D, k1E, k1F}, \
    {k2A, k2B, k2C, k2D, k2E, k2F}, \
    {KC_NO, KC_NO, KC_NO, k3D, k3E, k3F}, \
    {k4A, k4B, k4C, k4D, k4E, KC_NO}, \
    {k5A, k5B, k5C, k5D, k5E, k5F}, \
    {k6A, k6B, k6C, k6D, k6E, k6F}, \
    {k7A, k7B, k7C, k7D, k7E, k7F}, \
    {KC_NO, KC_NO, KC_NO, k8D, k8E, k8F}, \
    {k9A, k9B, k9C, k9D, k9E, KC_NO} \
}
