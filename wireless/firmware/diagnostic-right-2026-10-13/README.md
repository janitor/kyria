# Right-half power diagnostic firmware

This is the diagnostic image flashed to the right Halcyon Kyria wireless
controller with a CR1632 battery board and no encoder on 2026-10-13. It does
not replace the existing firmware files in the parent directory.

The only source revision changed from the current right-half firmware is
`splitkb/zmk-halcyon-module`: `d5ed4c1ec8028905bb3cc3705f3770e09bfd84de`
to `a5adc646208d733856042eacb371e1556fe0e044`. This upstream change
selects the key matrix directly and disables the unused NC-pin scanner and
composite scanner when no encoder module is present. The ZMK fork stays pinned
to `efbf0195bb2fac61c47896e3b7d5d3165679bc33`. `west.yml` and
`halcyon_kyria.keymap` are copies of the exact inputs used for this build.

The right-half build completed successfully in the
`zmkfirmware/zmk-dev-arm:4.1-branch` container. The generated devicetree
selects `kscan_matrix` and marks both `kscan_halcyon` and `kscan_composite`
disabled. The generated configuration retains deep sleep after 900,000 ms,
forced power-off after a suspend error, and battery-mode disabling of RGB
underglow and external power.

The upstream commit describes removal of unnecessary NC-pin scanning; it does
not claim a battery-life fix. Whether this changes power use on this keyboard
remains unmeasured. After flashing, the right controller was
reset once as Splitkb's wireless guide instructs. The controller enumerated
over USB as a ZMK device, and the user confirmed that both halves typed
through the dongle. Compare runtime using a fresh CR1632 from the same batch
as the left half.

Battery observation on 2026-10-13: the right-half cell measured above 3 V
after flashing (exact voltage and measurement conditions were not recorded).
This is the baseline for comparing later measurements on the same cell.
