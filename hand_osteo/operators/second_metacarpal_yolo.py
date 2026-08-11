from monai.deploy.core import Fragment, InputContext, Operator, OperatorSpec, OutputContext


class SecondMetacarpalYOLOOperator(Operator):
    input_name = "study_selected_series_list"
    output_name = "second_metacarpal_detection"

    def __init__(self, fragment: Fragment, *args, **kwargs):
        super().__init__(fragment, *args, **kwargs)

    def setup(self, spec: OperatorSpec):
        spec.input(self.input_name)
        spec.output(self.output_name)

    def compute(self, op_input: InputContext, op_output: OutputContext, context):
        print("SecondMetacarpalYOLOOperator: 2nd metacarpal")
        op_input.receive(self.input_name)
        op_output.emit({"label": "second_metacarpal"}, self.output_name)
