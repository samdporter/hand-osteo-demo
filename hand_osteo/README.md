# HandOsteo MAP

This is a minimal MONAI Deploy application shape for hand X-ray processing.

The deployment target is a Linux x86-64 DGX with Tesla V100 GPUs, an NVIDIA 555.42.06 driver, and a CUDA 12.2-level host environment. The MAP stack is deliberately frozen at MONAI Deploy App SDK 2.0.0 and Holoscan 2.0.0 because that release line uses the CUDA 12.2, TensorRT 8.6, and PyTorch 2.1 generation that still supports Volta GPUs.

`pyproject.toml` is the local project definition. `requirements.txt` is also consumed by the MAP packager, so both files carry the same exact pins. Holoscan 2.0.0 includes the matching `monai-deploy` command; do not add the standalone Holoscan 2.9 CLI to this environment.

## DGX prerequisites

- Ubuntu 22.04, or another x86-64 Linux distribution with glibc 2.35 or newer
- Python 3.11
- Docker with the buildx plugin
- NVIDIA Container Toolkit
- Access to PyPI and `nvcr.io` while installing and packaging

Install the SDK in the Linux/Python 3.11 environment:

```bash
python3.11 -m pip install -r hand_osteo/requirements.txt
python3.11 -m pip check
monai-deploy version
```

The version command should report Holoscan SDK 2.0.0 and MONAI Deploy App SDK 2.0.0.

Build the MAP from the repository root:

```bash
./package.sh
```

The script pulls the Holoscan `v2.0.0-dgpu` base image. Its packager platform is `x64-workstation`, the value accepted by the Holoscan 2.0 CLI.

## The model

`models/second_metacarpal.ts` is a fake placeholder model. `package.sh` passes it to the packager with `--models`, which copies it into the MAP. The application reads the path back as `context.model_path` and hands it to `SecondMetacarpalYOLOOperator`, which prints it.

Run the packaged MAP, using the image tag printed by the packager:

```bash
monai-deploy run hand_osteo-x64-workstation-dgpu-linux-amd64:0.1.0 \
  -i ./input \
  -o ./output
```

Build any TensorRT engine on a V100. TensorRT engine files are tied to the GPU architecture and must not be copied from an Ampere or newer system.
