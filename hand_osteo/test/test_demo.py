from pathlib import Path
import sys
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

    def test_pyproject_is_dependency_source(self):
        project = (ROOT / "pyproject.toml").read_text()
        self.assertIn('requires-python = "==3.11.*"', project)
        self.assertIn('"monai-deploy-app-sdk==2.0.0"', project)
        requirements = (ROOT / "requirements.txt").read_text()
        self.assertIn("monai-deploy-app-sdk==2.0.0", requirements)

    def test_package_script_uses_monai_deploy_base_image(self):
        source = (ROOT.parent / "package.sh").read_text()
        self.assertIn("nvcr.io/nvidia/clara-holoscan/holoscan:v2.0.0-dgpu", source)
        self.assertIn('docker pull "$BASE_IMAGE"', source)
        self.assertIn('monai-deploy package "$APP_DIR"', source)
        self.assertIn('--platform "$PLATFORM"', source)
        self.assertIn('--sdk-version "$SDK_VERSION"', source)

if __name__ == "__main__":
    unittest.main()
