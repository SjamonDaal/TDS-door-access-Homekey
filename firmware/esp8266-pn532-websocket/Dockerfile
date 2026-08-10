# PlatformIO build environment for the ESP8266/ESP32 reader firmware. The
# source tree (including a locally created include/secrets.h) is bind-mounted
# at run time rather than copied in, so this image never bakes in secrets and
# never needs rebuilding when the firmware source changes. See build-docker.
FROM python:3.11-slim

# esptool (bundled by the espressif32/espressif8266 platform packages) needs
# these at run time; PlatformIO invokes it with the system interpreter rather
# than a private venv, so they must be installed here explicitly.
RUN pip install --no-cache-dir platformio esptool

WORKDIR /firmware
ENTRYPOINT ["pio"]
CMD ["run"]
