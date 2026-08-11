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
        op_input.receive(self.input_detection)
        op_input.receive(self.input_measurements)
        op_output.emit(b"%PDF-1.4\nHandOsteo report\n%%EOF\n", self.output_name)
