#!/usr/bin/env bash
# Offline tests in the gcc:12 Docker image (needs network: they read the live catalog and download one zip).
#   tests/run.sh            the wrapper host test, then each fake device in tests/devices/
# A fake device is a shell script that builds the device's files inside the container: MPC.settings (the real format,
# trimmed), plugin folders, a stub systemctl. FS_ANY=1 lets the container's overlay filesystem count as internal storage.
# Add one for your model (copy its MPC.settings layout from the device.txt the plugin writes) and send it with your PR.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
MV="${MPC_VST:-$here/../mpc-vst-plugins}"
python3 "$MV/tools/gen_vst.py" "$here/vst/vst.json" --params-h >/dev/null
docker run --rm -v "$here":/p -v "$MV":/mv:ro -w /p gcc:12 bash -c '
set -e
SAN="-fsanitize=address,undefined -fno-omit-frame-pointer -g -O1"
gcc $SAN -std=gnu11 -w -Ivst/build src/manager.c /mv/tools/host_test.c /mv/wrapper/vst2_wrap.c -lpthread -ldl -lm -o /tmp/host_test
(cd /tmp && ./host_test | tail -n 1)
gcc $SAN -DFS_ANY=1 -std=gnu11 -w src/manager.c tests/drive.c -lpthread -ldl -o /tmp/drive
for dev in tests/devices/*.sh; do
  echo "== $dev"
  # each device starts from a clean filesystem
  rm -rf /media /sdcard /tmp/pluginmgr; mkdir -p /media
  sh "$dev" && /tmp/drive && grep -E "location|target|problem" /tmp/pluginmgr/device.txt
done'
