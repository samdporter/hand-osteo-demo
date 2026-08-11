# HandOsteo MAP demo

This is a code-shape demo only. It does not find bones, measure joints, or produce clinical output.

The app is structured for MONAI Deploy App SDK 2.0.0 packaging on Linux with Python 3.11.

`pyproject.toml` is the local project definition. `requirements.txt` is kept as the MAP packager input.

Install the SDK:

```bash
python3.11 -m pip install -r requirements.txt
```

Print the placeholder workflow:

```bash
python3.11 app.py --demo
```

Run the un-packaged app with DICOM input:

```bash
monai-deploy exec app.py -i ./input -o ./output
```

Build a MAP on the Linux x86-64 host:


```bash
monai-deploy package . \
  --config ./config.yaml \
  --tag hand_osteo:0.0.1 \
  --platform x86_64 \
  --sdk-version 2.0.0 \
  --log-level DEBUG
```

Run the packaged MAP, using the image tag printed by the packager:

```bash
monai-deploy run hand_osteo-x64-workstation-dgpu-linux-amd64:0.0.1 \
  -i ./input \
  -o ./output
```
