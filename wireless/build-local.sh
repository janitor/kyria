#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
workspace_root="${KYRIA_ZMK_WORKSPACE:-/tmp/kyria-zmk-build}"
image="zmkfirmware/zmk-dev-arm:4.1-branch"

mkdir -p "$workspace_root/config" "$script_dir/firmware"
cp -R "$script_dir/config/." "$workspace_root/config/"

docker image inspect "$image" >/dev/null 2>&1 || docker pull "$image"

if [[ ! -f "$workspace_root/.west/config" ]]; then
    docker run --rm -v "$workspace_root:/workspaces/kyria-zmk" \
        -w /workspaces/kyria-zmk "$image" west init -l config
fi

docker run --rm -v "$workspace_root:/workspaces/kyria-zmk" \
    -w /workspaces/kyria-zmk "$image" west update -n -o=--depth=1

docker run --rm -v "$workspace_root:/workspaces/kyria-zmk" \
    -w /workspaces/kyria-zmk "$image" /bin/bash -lc '
        set -euo pipefail
        west zephyr-export
        cd zmk/app
        west build -d /workspaces/kyria-zmk/build/dongle -p always \
            -b halcyon_dongle//zmk -S studio-rpc-usb-uart -- \
            -DSHIELD=halcyon_kyria_dongle \
            -DZMK_CONFIG=/workspaces/kyria-zmk/config \
            -DCONFIG_ZMK_STUDIO=y
        west build -d /workspaces/kyria-zmk/build/left -p always \
            -b halcyon_wireless//zmk -- \
            -DSHIELD="halcyon_kyria_left mod_battery_coincell" \
            -DZMK_CONFIG=/workspaces/kyria-zmk/config \
            -DCONFIG_ZMK_SPLIT_ROLE_CENTRAL=n
        west build -d /workspaces/kyria-zmk/build/right -p always \
            -b halcyon_wireless//zmk -- \
            -DSHIELD="halcyon_kyria_right mod_battery_coincell" \
            -DZMK_CONFIG=/workspaces/kyria-zmk/config
    '

cp "$workspace_root/build/dongle/zephyr/zmk.uf2" \
    "$script_dir/firmware/kyria-dongle-wellum36.uf2"
cp "$workspace_root/build/left/zephyr/zmk.uf2" \
    "$script_dir/firmware/kyria-left-coincell.uf2"
cp "$workspace_root/build/right/zephyr/zmk.uf2" \
    "$script_dir/firmware/kyria-right-coincell.uf2"

(
    cd "$script_dir/firmware"
    shasum -a 256 ./*.uf2 | tee SHA256SUMS
)
