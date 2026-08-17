from io import BytesIO

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

from monai.deploy.core import Fragment, InputContext, Operator, OperatorSpec, OutputContext


class PDFReportOperator(Operator):
    input_series = "study_selected_series_list"
    input_detection = "second_metacarpal_detection"
    input_measurements = "mcp_measurements"
    output_name = "pdf_bytes"

    def __init__(self, fragment: Fragment, *args, **kwargs):
        super().__init__(fragment, *args, **kwargs)

    def setup(self, spec: OperatorSpec):
        spec.input(self.input_series)
        spec.input(self.input_detection)
        spec.input(self.input_measurements)
        spec.output(self.output_name)

    def compute(self, op_input: InputContext, op_output: OutputContext, context):
        print("PDFReportOperator: PDF bytes")
        op_input.receive(self.input_series)
        detection = op_input.receive(self.input_detection)
        measurements = op_input.receive(self.input_measurements)
        op_output.emit(self._build_pdf(detection, measurements), self.output_name)

    def _build_pdf(self, detection, measurements) -> bytes:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=LETTER)
        _, height = LETTER

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(72, height - 72, "HandOsteo Report")

        pdf.setFont("Helvetica", 11)
        pdf.drawString(72, height - 108, f"Detection: {detection}")
        pdf.drawString(72, height - 126, f"MCP measurements: {measurements}")

        pdf.showPage()
        pdf.save()
        return buffer.getvalue()
