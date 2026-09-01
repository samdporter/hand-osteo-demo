from pathlib import Path

from monai.deploy.core import Fragment, InputContext, Operator, OperatorSpec, OutputContext


class LoaderOperator(Operator):
    output_name = "data"

    def __init__(self, fragment: Fragment, *args, input_path: Path, **kwargs):
        self.input_path = input_path
        super().__init__(fragment, *args, **kwargs)

    def setup(self, spec: OperatorSpec):
        spec.output(self.output_name)

    def compute(self, op_input: InputContext, op_output: OutputContext, context):
        data = self.input_path.read_bytes()
        op_output.emit(data, self.output_name)


class ProcessorOperator(Operator):
    input_name = "data"
    output_name = "result"

    def __init__(self, fragment: Fragment, *args, model_path: Path, **kwargs):
        self.model_path = model_path
        super().__init__(fragment, *args, **kwargs)

    def setup(self, spec: OperatorSpec):
        spec.input(self.input_name)
        spec.output(self.output_name)

    def compute(self, op_input: InputContext, op_output: OutputContext, context):
        data = op_input.receive(self.input_name)
        op_output.emit(data, self.output_name)


class WriterOperator(Operator):
    input_name = "result"

    def __init__(self, fragment: Fragment, *args, output_path: Path, **kwargs):
        self.output_path = output_path
        super().__init__(fragment, *args, **kwargs)

    def setup(self, spec: OperatorSpec):
        spec.input(self.input_name)

    def compute(self, op_input: InputContext, op_output: OutputContext, context):
        result = op_input.receive(self.input_name)
        self.output_path.write_bytes(result)
