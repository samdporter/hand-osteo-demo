from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import DEMO_STEPS, demo_output


class HandOsteoDemoTests(unittest.TestCase):
    def test_demo_output_lists_pipeline_in_order(self):
        self.assertEqual(
            demo_output().splitlines(),
            ["HandOsteo demo", *DEMO_STEPS],
        )

    def test_app_declares_native_monai_operators(self):
        source = (ROOT / "app.py").read_text()
        for name in (
            "DICOMDataLoaderOperator",
            "DICOMSeriesSelectorOperator",
            "DICOMEncapsulatedPDFWriterOperator",
        ):
            self.assertIn(name, source)

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
        self.assertIn("title: HandOsteo Demo", config)
        self.assertIn("version: 0.0.1", config)
        self.assertIn("from app import build_app", main)

    def test_pyproject_is_dependency_source(self):
        project = (ROOT / "pyproject.toml").read_text()
        self.assertIn('requires-python = "==3.11.*"', project)
        self.assertIn('"monai-deploy-app-sdk==2.0.0"', project)
        requirements = (ROOT / "requirements.txt").read_text()
        self.assertIn("monai-deploy-app-sdk==2.0.0", requirements)

    def test_cuda_dockerfile_targets_python_311(self):
        source = (ROOT / "Dockerfile").read_text()
        self.assertIn("nvcr.io/nvidia/cuda:12.2.0-runtime-ubuntu22.04", source)
        self.assertIn("python3.11", source)


if __name__ == "__main__":
    unittest.main()
