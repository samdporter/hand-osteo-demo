from pathlib import Path

from monai.deploy.core import Application


class MyApp(Application):
    name = "my_app"
    description = "Example MONAI Deploy application"
    version = "0.1.0"

    def compose(self):
        context = Application.init_app_context(self.argv)

        loader = LoaderOperator(self, input_path=Path(context.input_path), name="loader")
        processor = ProcessorOperator(self, model_path=context.model_path, name="processor")
        writer = WriterOperator(self, output_path=Path(context.output_path), name="writer")

        self.add_flow(loader, processor, {("data", "data")})
        self.add_flow(processor, writer, {("result", "result")})
