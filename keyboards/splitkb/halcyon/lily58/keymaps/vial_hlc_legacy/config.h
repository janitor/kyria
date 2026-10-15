/* SPDX-License-Identifier: GPL-2.0-or-later */
/* Copyright 2023 splitkb.com <support@splitkb.com> */

#pragma once

#define VIAL_KEYBOARD_UID {0x14, 0x27, 0x8E, 0x26, 0xFA, 0x62, 0xD7, 0x01}

#define VIAL_UNLOCK_COMBO_ROWS { 0, 6 }
#define VIAL_UNLOCK_COMBO_COLS { 5, 5 }

#define RGB_MATRIX_FRAMEBUFFER_EFFECTS
#define RGB_MATRIX_KEYPRESSES

#define DYNAMIC_KEYMAP_LAYER_COUNT 8

#define HALCYON_LEGACY

#undef MATRIX_ROWS
#define MATRIX_ROWS 12
#define LAYOUT_lily58_hlc(k0A, k0B, k0C, k0D, k0E, k0F, k6F, k6E, k6D, k6C, k6B, k6A, k1A, k1B, k1C, k1D, k1E, k1F, k7F, k7E, k7D, k7C, k7B, k7A, k2A, k2B, k2C, k2D, k2E, k2F, k8F, k8E, k8D, k8C, k8B, k8A, k3A, k3B, k3C, k3D, k3E, k3F, k4B, k10B, k9F, k9E, k9D, k9C, k9B, k9A, k4C, k4D, k4E, k4F, k10F, k10E, k10D, k10C, k5A, k5B, k5C, k5D, k5E, k11A, k11B, k11C, k11D, k11E) { \
    {k0A, k0B, k0C, k0D, k0E, k0F}, \
    {k1A, k1B, k1C, k1D, k1E, k1F}, \
    {k2A, k2B, k2C, k2D, k2E, k2F}, \
    {k3A, k3B, k3C, k3D, k3E, k3F}, \
    {KC_NO, k4B, k4C, k4D, k4E, k4F}, \
    {k5A, k5B, k5C, k5D, k5E, KC_NO}, \
    {k6A, k6B, k6C, k6D, k6E, k6F}, \
    {k7A, k7B, k7C, k7D, k7E, k7F}, \
    {k8A, k8B, k8C, k8D, k8E, k8F}, \
    {k9A, k9B, k9C, k9D, k9E, k9F}, \
    {KC_NO, k10B, k10C, k10D, k10E, k10F}, \
    {k11A, k11B, k11C, k11D, k11E, KC_NO} \
}
