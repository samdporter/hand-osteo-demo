#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${APP_DIR:-$ROOT_DIR/hand_osteo}"
CONFIG_PATH="${CONFIG_PATH:-$APP_DIR/config.yaml}"
TAG="${HAND_OSTEO_TAG:-hand_osteo:0.1.0}"
PLATFORM="${MONAI_DEPLOY_PLATFORM:-x86_64}"
SDK_VERSION="${MONAI_DEPLOY_SDK_VERSION:-2.0.0}"
LOG_LEVEL="${MONAI_DEPLOY_LOG_LEVEL:-DEBUG}"
BASE_IMAGE="${MONAI_DEPLOY_BASE_IMAGE:-nvcr.io/nvidia/clara-holoscan/holoscan:v2.0.0-dgpu}"

command -v docker >/dev/null 2>&1 || {
    echo "docker is required" >&2
    exit 1
}

command -v monai-deploy >/dev/null 2>&1 || {
    echo "monai-deploy is required in the active Python environment" >&2
    exit 1
}

test -d "$APP_DIR" || {
    echo "application directory not found: $APP_DIR" >&2
    exit 1
}

test -f "$CONFIG_PATH" || {
    echo "config file not found: $CONFIG_PATH" >&2
    exit 1
}

docker pull "$BASE_IMAGE"

exec monai-deploy package "$APP_DIR" \
    --config "$CONFIG_PATH" \
    --tag "$TAG" \
    --platform "$PLATFORM" \
    --sdk-version "$SDK_VERSION" \
    --log-level "$LOG_LEVEL"
