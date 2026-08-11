#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

BASE_IMAGE="nvcr.io/nvidia/clara-holoscan/holoscan:v2.0.0-dgpu"

docker pull "$BASE_IMAGE"

monai-deploy package hand_osteo \
    --config hand_osteo/config.yaml \
    --models models/second_metacarpal.ts \
    --tag hand_osteo:0.1.0 \
    --platform x64-workstation \
    --sdk-version 2.0.0 \
    --base-image "$BASE_IMAGE"
