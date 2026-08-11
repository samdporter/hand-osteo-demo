# HandOsteo MAP

This is a minimal MONAI Deploy application shape for hand X-ray processing.

The app is structured for MONAI Deploy App SDK 2.0.0 packaging on Linux with Python 3.11.

`pyproject.toml` is the local project definition. `requirements.txt` is kept as the MAP packager input.

Install the SDK in the Linux/Python 3.11 environment:

```bash
python3.11 -m pip install -r requirements.txt
```

Build the MAP from the repository root:

```bash
./package.sh
```

The script pulls the MONAI Deploy SDK 2.0.0 x86-64 base image before running the packager. Set `HAND_OSTEO_TAG`, `MONAI_DEPLOY_BASE_IMAGE`, `MONAI_DEPLOY_PLATFORM`, or `MONAI_DEPLOY_LOG_LEVEL` to override defaults.

Run the packaged MAP, using the image tag printed by the packager:

```bash
monai-deploy run hand_osteo-x64-workstation-dgpu-linux-amd64:0.1.0 \
  -i ./input \
  -o ./output
```
