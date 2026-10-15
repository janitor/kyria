# Kyria rev4 firmware and keyboard layout

This repository contains my Halcyon Kyria rev4 setup:

- [`wireless/`](wireless/) has the ZMK configuration for two Halcyon Wireless
  Controllers, CR1632 coin-cell boards, and a Halcyon USB-C dongle. It includes
  the keymap, pinned upstream revisions, and build targets. This is the
  configuration relevant to the right-half battery-drain support case.
- [`keyboards/splitkb/halcyon/kyria/keymaps/`](keyboards/splitkb/halcyon/kyria/keymaps/)
  has wired QMK keymaps. These are separate from the wireless ZMK firmware.
- [`macos-layout/`](macos-layout/) has the companion macOS keyboard layout and
  Karabiner rule.

Case and stand models are kept outside this public repository because their
redistribution terms have not been confirmed.

The QMK userspace base comes from
[splitkb/qmk_userspace](https://github.com/splitkb/qmk_userspace). The
upstream instructions below describe that base; my wireless configuration is
documented separately in [`wireless/README.md`](wireless/README.md).

## Upstream QMK userspace instructions

This is the splitkb userspace repository. It allows for an external set of QMK keymaps with **Halcyon modules** to be defined and compiled without having to fork the main QMK or Vial repositories. 

*If you want to compile standard firmware without any Halcyon modules, you can use the [main qmk_userspace repo](https://github.com/qmk/qmk_userspace). If you use the Halcyon to Promicro adapter board without any Halcyon modules you can use the converter without this repository.*

## Supported Keyboards

Supported controllers:

| Controller name |
| :--- |
| Halcyon Wired controller |


Supported keyboards:

| Keyboard name | Keyboard variable |
| :--- | :--- |
| Halcyon Kyria (rev4) | `splitkb/halcyon/kyria/rev4` |
| Halcyon Elora (rev2) | `splitkb/halcyon/elora/rev2` |
| Halcyon Corne (rev2) | `splitkb/halcyon/corne/rev2` |
| Halcyon Ferris (rev1) | `splitkb/halcyon/ferris/rev1` |
| Halcyon Lily58 (rev2) | `splitkb/halcyon/lily58/rev2` |
| Aurora Sweep (rev1)* | `splitkb/aurora/sweep/rev1` |
| Aurora Lily58 (rev1)* | `splitkb/aurora/lily58/rev1` |
| Aurora Corne (rev1)* | `splitkb/aurora/corne/rev1` |
| Aurora Helix (rev1)* | `splitkb/aurora/helix/rev1` |
| Aurora Sofle v2 (rev1)* | `splitkb/aurora/sofle_v2/rev1` |
| Kyria (rev3)* | `splitkb/kyria/rev3` |

*Requires the Halcyon converter


Supported converters:

| Converter name | Converter variable | Convert command |
| :--- | :--- | :--- |
| Halcyon | `halcyon` | `CONVERT_TO=halcyon` |


Supported modules:

| Module name | Module variable |
| :--- | :--- |
| [Halcyon TFT LCD Display Module](https://splitkb.com/products/halcyon-tft-lcd-display-module) | `HLC_TFT_DISPLAY` |
| [Halcyon Rotary Encoder Module](https://splitkb.com/products/halcyon-rotary-encoder-module) | `HLC_ENCODER` |
| [Halcyon Rotary Encoder Module Revision 2](https://splitkb.com/products/halcyon-rotary-encoder-module) | `HLC_ENCODER_REV2` |
| [Halcyon Cirque Touchpad Module](https://splitkb.com/products/halcyon-cirque-touchpad-module) | `HLC_CIRQUE_TRACKPAD` |

If you want to add a keyboard which doesn't have support for Halcyon modules yet, please follow the [porting guide](docs/PORTING.md). Please follow the [initial setup](#initial-setup--prerequisites) and [build target](#how-to-configure-your-build-targets) steps from this readme first.

This repository contains keymaps for both upstream QMK (default_hlc) and Vial (vial_hlc). For the officially supported keyboards we will always provide these two keymaps. 


## Initial Setup & Prerequisites

Before configuring your keymaps or building firmware, you need to set up your build environment. 

1. **Fork this repository** to your own GitHub account. 
   - The default `halcyon` branch includes Vial support.
   - If you prefer upstream QMK without Vial, fork the `halcyon-qmk` branch instead.
2. **Clone the Vial repository** to your local machine:
   - For Vial:
     ```bash
     git clone --recursive https://github.com/vial-kb/vial-qmk
     ```
   - For upstream QMK:
     ```bash
     git clone --recursive https://github.com/qmk/qmk_firmware
     ```
3. **Set up QMK** using your cloned repository (see [QMK Docs](https://docs.qmk.fm/#/newbs) for more details):
   ```bash
   qmk setup -H path/to/your/qmk/repository
   ```
   When prompted whether to keep the existing repository, select **3**.
4. **Clone your forked userspace repository** to your local machine.
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/qmk_userspace
   ```
5. **Enable userspace in QMK config**: 
   Navigate into your cloned userspace directory and run:
   ```bash
   cd path/to/your/forked/qmk_userspace
   qmk config user.overlay_dir="$(realpath .)"
   ```
   This tells QMK where to find your userspace, regardless of your current working directory.

*Note: If you have already forked the `qmk/qmk_userspace` repository previously, see the [Adding to an Existing Fork](#adding-halcyon-support-to-an-existing-userspace-fork) section below.*


## How to Configure Your Build Targets

1. **Start fresh (Optional but recommended):** If you want to start completely from scratch without any default compile options, replace the `qmk.json` in the root folder with the provided `qmk_empty.json`.
2. **Create your keymap:** Navigate to `keyboards/<keyboard_name>/keymaps` and copy/paste the `default_hlc` or the `vial_hlc` or `vial_hlc_legacy` folder, if you still want to use vial. Rename it to your desired keymap name.  
    *(**Updating Keymaps:** If you modify an existing keymap (e.g., from the original Kyria, Elora, or Aurora), and want to use a Halcyon encoder module, make sure to **add the Halcyon Button mappings** and **Encoder mapping** as shown in [the porting guide](docs/PORTING.md#3-define-halcyon-button-mappings))*  
    *(If you're unsure what the exact `keyboard_name` is, you can run `qmk list-keyboards | grep <keyboard>`)*  
    *For existing Vial users, you should use the `vial_hlc_legacy` keymap as the location mapping is different in the newer version and this is not compatible with the new version. You would otherwise have to recreate your keymap in Vial. Otherwise you can use the newer `vial_hlc` keymap.*
3. **Add your keymap to the build targets** by running the following command:
   ```bash
   qmk userspace-add -kb <your_keyboard> -km <your_keymap> -e <halcyon_module>=1 -e TARGET=<filename>
   ```
   * *This command will automatically update your `qmk.json` file.*
   * **`filename`**: Choose a descriptive filename so you can easily differentiate between module firmware (e.g., `halcyon_kyria_default_encoder`).
   * **`halcyon_module`**: Replace this with one of the following environment variables depending on your hardware:

   | Module Variable | Description |
   | :--- | :--- |
   | `HLC_NONE` | You have a module installed on the *other* half, but not this half. |
   | `HLC_ENCODER` | You have an encoder module installed. |
   | `HLC_ENCODER_REV2` | You have a second revision encoder module installed. |
   | `HLC_TFT_DISPLAY` | You have a TFT RGB display installed. |
   | `HLC_CIRQUE_TRACKPAD` | You have a Cirque trackpad installed. |

#### Useful Userspace Commands
* **List configured targets:** `qmk userspace-list`
* **Show generated compile commands:** `qmk userspace-compile -n`
* **Remove a target:** `qmk userspace-remove -kb <your_keyboard> -km <your_keymap> -e <halcyon_module>=1 -e TARGET=<filename>`. You can also remove a target by removing the specific lines in the `qmk.json` file.


## Changing module behavior

Please see the [seperate docs](docs/MODULES.md).


## How to Build with GitHub Actions

The included workflow builds wired QMK targets only. It runs when manually
started; a push does not start it or publish a release. The wireless ZMK
configuration has separate local build instructions in `wireless/README.md`.

1. Go to the **Actions** tab of your forked GitHub repository and click **"I understand my workflows, go ahead and enable them"**.
2. Open **Build QMK firmware** and choose **Run workflow**.
3. Check that workflow run for its build results.


## How to Build Locally

Assuming you have completed the initial setup and configured your build targets, you can compile locally.

**To build all userspace targets at once:**
```bash
qmk userspace-compile
```

**To compile a specific target manually:**
```bash
qmk compile -kb <your_keyboard> -km <your_keymap> -e <your_module>=1 -e TARGET=<filename>
```
*Tip: use `qmk userspace-compile -n` to get the exact compile command*

## Extra Info & Advanced Configuration

### Modifying GitHub Actions
To point GitHub Actions to a different QMK repository or branch, modify
`.github/workflows/build_binaries.yaml`.

For example, to override the `build` job to use the QMK branch (which is already done in the `halcyon-qmk` branch):
```yaml
    with:
      qmk_repo: qmk/qmk_firmware
      qmk_ref: master
```
*Note: Our Halcyon module code should work fine with the main QMK repository, but it may break if QMK introduces upstream breaking changes. We track QMK updates in the `halcyon-qmk` branch.*

### Adding Halcyon support to an Existing Userspace Fork

If you already have a custom userspace fork of `qmk/qmk_userspace`, you can merge the Splitkb additions manually.

#### Option A: Adding the Splitkb Upstream Branch

1. Add this repository as a remote:
   ```bash
   git remote add splitkb https://github.com/splitkb/qmk_userspace.git
   ```
2. Fetch the upstream branches:
   ```bash
   git fetch splitkb
   ```
3. Create a local branch based on the appropriate upstream branch:
   - **Vial:**
     ```bash
     git checkout -b halcyon splitkb/halcyon
     ```
   - **Upstream QMK:**
     ```bash
     git checkout -b halcyon-qmk splitkb/halcyon-qmk
     ```
4. Make your changes and push your branch:
   ```bash
   git push -u origin <branch-name>
   ```
   Replace `<branch-name>` with either `halcyon` or `halcyon-qmk`.

#### Option B: Copying files to your existing branch
1. Clone or download the files from the Splitkb fork.
2. Copy and/or merge `users/halcyon_modules/rules.mk` and the entire `users/halcyon_modules/splitkb/` folder into your personal user folder.

**⚠️ Warning:** We use some quantum functions in our userspace. If your existing userspace relies heavily on custom quantum functions, you may encounter compile conflicts. If you restrict yourself to `_user` functions, you should be fine.
