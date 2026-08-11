def build_app():
    from pathlib import Path

    from monai.deploy.conditions import CountCondition
    from monai.deploy.core import Application
    from monai.deploy.operators import DICOMEncapsulatedPDFWriterOperator
    from monai.deploy.operators.dicom_data_loader_operator import DICOMDataLoaderOperator
    from monai.deploy.operators.dicom_series_selector_operator import DICOMSeriesSelectorOperator
    from monai.deploy.operators.dicom_utils import EquipmentInfo, ModelInfo

    from operators.mcp_measurer import MCPMeasurer
    from operators.pdf_report import PDFReportOperator
    from operators.second_metacarpal_yolo import SecondMetacarpalYOLOOperator

    class HandOsteoApp(Application):
        name = "hand_osteo"
        description = "HandOsteo MONAI Deploy application"
        version = "0.1.0"

        def compose(self):
            context = Application.init_app_context(self.argv)
            loader = DICOMDataLoaderOperator(
                self,
                CountCondition(self, 1),
                input_folder=Path(context.input_path),
                name="dicom_loader",
            )
            selector = DICOMSeriesSelectorOperator(
                self,
                rules=SERIES_RULES,
                name="dicom_selector",
            )
            detector = SecondMetacarpalYOLOOperator(
                self,
                model_path=context.model_path,
                name="second_metacarpal_yolo",
            )
            measurer = MCPMeasurer(self, name="mcp_measurer")
            report = PDFReportOperator(self, name="pdf_report")
            writer = DICOMEncapsulatedPDFWriterOperator(
                self,
                output_folder=Path(context.output_path),
                model_info=ModelInfo(
                    creator="HandOsteo",
                    name=self.name,
                    version=self.version,
                ),
                equipment_info=EquipmentInfo(
                    manufacturer="HandOsteo",
                    manufacturer_model=self.name,
                ),
                copy_tags=True,
                name="dicom_pdf_writer",
            )

            self.add_flow(loader, selector, {("dicom_study_list", "dicom_study_list")})
            self.add_flow(
                selector,
                detector,
                {("study_selected_series_list", "study_selected_series_list")},
            )
            self.add_flow(
                detector,
                measurer,
                {("second_metacarpal_detection", "second_metacarpal_detection")},
            )
            self.add_flow(measurer, report, {("mcp_measurements", "mcp_measurements")})
            self.add_flow(
                selector,
                report,
                {("study_selected_series_list", "study_selected_series_list")},
            )
            self.add_flow(
                detector,
                report,
                {("second_metacarpal_detection", "second_metacarpal_detection")},
            )
            self.add_flow(report, writer, {("pdf_bytes", "pdf_bytes")})
            self.add_flow(
                selector,
                writer,
                {("study_selected_series_list", "study_selected_series_list")},
            )

    return HandOsteoApp


SERIES_RULES = """
{
    "selections": [
        {
            "name": "Hand X-ray series",
            "conditions": {
                "Modality": "DX",
                "BodyPartExamined": "HAND"
            }
        }
    ]
}
"""
