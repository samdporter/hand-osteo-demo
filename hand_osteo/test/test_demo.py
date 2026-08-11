from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class HandOsteoTests(unittest.TestCase):
    def test_app_declares_native_monai_operators(self):
        source = (ROOT / "app.py").read_text()
        for name in (
            "DICOMDataLoaderOperator",
            "DICOMSeriesSelectorOperator",
            "DICOMEncapsulatedPDFWriterOperator",
        ):
            self.assertIn(name, source)

    def test_app_has_no_print_demo_entrypoint(self):
        source = (ROOT / "app.py").read_text()
        self.assertNotIn("DEMO_STEPS", source)
        self.assertNotIn("--demo", source)

    def test_series_rules_target_hand_xray(self):
        source = (ROOT / "app.py").read_text()
        self.assertIn('"name": "Hand X-ray series"', source)
        self.assertIn('"Modality": "DX"', source)
        self.assertNotIn('"Modality": "MR"', source)

    def test_local_operator_files_declare_ports(self):
        contracts = {
            "second_metacarpal_yolo.py": (
                "SecondMetacarpalYOLOOperator",
                "study_selected_series_list",
                "second_metacarpal_detection",
            ),
            "mcp_measurer.py": (
                "MCPMeasurer",
                "second_metacarpal_detection",
                "mcp_measurements",
            ),
            "pdf_report.py": (
                "PDFReportOperator",
                "mcp_measurements",
                "pdf_bytes",
            ),
        }
        for filename, expected in contracts.items():
            source = (ROOT / "operators" / filename).read_text()
            for value in expected:
                self.assertIn(value, source)

    def test_pdf_placeholder_has_pdf_signature(self):
        source = (ROOT / "operators" / "pdf_report.py").read_text()
        self.assertIn("%PDF-1.4", source)

    def test_map_packaging_files_are_present(self):
        config = (ROOT / "config.yaml").read_text()
        main = (ROOT / "__main__.py").read_text()
        self.assertIn("title: HandOsteo\n", config)
        self.assertIn("version: 0.1.0", config)
        self.assertIn("from app import build_app", main)

    def test_dependency_manifests_pin_the_v100_stack(self):
        expected = [
            "monai-deploy-app-sdk==2.0.0",
            "holoscan==2.0.0",
        ]
        project = tomllib.loads((ROOT / "pyproject.toml").read_text())
        self.assertEqual(project["project"]["requires-python"], "==3.11.*")
        self.assertEqual(project["project"]["dependencies"], expected)

        requirements = (ROOT / "requirements.txt").read_text().splitlines()
        self.assertEqual(requirements, expected)

    def test_package_script_pins_the_v100_packaging_contract(self):
        source = (ROOT.parent / "package.sh").read_text()
        base_image = (
            "nvcr.io/nvidia/clara-holoscan/holoscan:v2.0.0-dgpu"
            "@sha256:20adbccd2c7b12dfb1798f6953f071631c3b85cd337858a7506f8e420add6d4a"
        )
        self.assertIn('PLATFORM="${MONAI_DEPLOY_PLATFORM:-x64-workstation}"', source)
        self.assertIn('SDK_VERSION="${MONAI_DEPLOY_SDK_VERSION:-2.0.0}"', source)
        self.assertIn(
            f'BASE_IMAGE="${{MONAI_DEPLOY_BASE_IMAGE:-{base_image}}}"',
            source,
        )
        self.assertIn('docker pull "$BASE_IMAGE"', source)
        self.assertIn('monai-deploy package "$APP_DIR"', source)
        self.assertIn('--platform "$PLATFORM"', source)
        self.assertIn('--sdk-version "$SDK_VERSION"', source)
        self.assertIn('--base-image "$BASE_IMAGE"', source)
        self.assertNotIn("CUDA_VERSION", source)
        self.assertNotIn("--cuda", source)


if __name__ == "__main__":
    unittest.main()
