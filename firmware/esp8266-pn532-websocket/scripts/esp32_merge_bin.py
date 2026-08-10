# PlatformIO post-build step for the esp32 environment (platformio.ini).
#
# Unlike the ESP8266 build, where the Arduino core already links the
# bootloader into one firmware.bin flashable at 0x0, an ESP32 build produces
# separate bootloader, partition table and application images that normally
# need `pio run --target upload` to place at their correct offsets. This
# combines them into one ${PROGNAME}-merged.bin flashable at 0x0 with a
# single `esptool.py write_flash 0x0 ...` command, so a machine with only
# esptool installed (no PlatformIO, no compiler toolchain) can flash a build
# produced elsewhere, e.g. by build-docker.
Import("env")


def merge_bin(source, target, env):
    output_path = env.subst("$BUILD_DIR/${PROGNAME}-merged.bin")
    firmware_path = env.subst("$BUILD_DIR/${PROGNAME}.bin")
    app_offset = env.get("ESP32_APP_OFFSET", "0x10000")
    flash_images = env.Flatten(env.subst(env.get("FLASH_EXTRA_IMAGES", [])))

    command = [
        env.subst("$PYTHONEXE"),
        env.subst("$OBJCOPY"),
        "--chip", env.get("BOARD_MCU"),
        "merge_bin",
        "--output", output_path,
    ]
    command += flash_images
    command += [app_offset, firmware_path]

    env.Execute(" ".join(command))
    print("[esp32_merge_bin] wrote " + output_path)


env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", merge_bin)
