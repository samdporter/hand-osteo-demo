docker pull nvcr.io/nvidia/clara-holoscan/holoscan:v2.0.0-dgpu

monai-deploy package app_demo.py --models models/second_metacarpal.ts --tag app_demo:0.1.0 --platform x64-workstation --sdk-version 2.0.0 --base-image nvcr.io/nvidia/clara-holoscan/holoscan:v2.0.0-dgpu

monai-deploy run app_demo:0.1.0 input output
