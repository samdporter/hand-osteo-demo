from monai.deploy.core import Fragment, InputContext, Operator, OperatorSpec, OutputContext


class MCPMeasurer(Operator):
    input_name = "second_metacarpal_detection"
    output_name = "mcp_measurements"

    def __init__(self, fragment: Fragment, *args, **kwargs):
        super().__init__(fragment, *args, **kwargs)

    def setup(self, spec: OperatorSpec):
        spec.input(self.input_name)
        spec.output(self.output_name)

    def compute(self, op_input: InputContext, op_output: OutputContext, context):
        print("MCPMeasurer: MCP measurements")
        op_input.receive(self.input_name)
        op_output.emit({"status": "placeholder"}, self.output_name)
