import fire

from template import Template
from generator import Generator
from zipper import Zipper
from test_cases import fetch_test_cases

class QGen:
    """
        QGen is a tool to generate competitive programming problems for the Andalus Judge.
        It takes a template and generates a problem based on it.
        The template and all examples can be found in the samples folder.
    """

    def generate(self, template_path, output_path="./outputs", format_file="./format/format.docx"):
        """
            Generate a problem based on a template.
            The template can be found in the samples folder.
            The output is saved in the outputs folder.
        """
        template = Template(template_path)
        for problem in template.get_problems():
            generator = Generator(problem, format_file)
            pdf_path = generator.generate()
            
            additional_test_cases_generator = None
            if "uva_id" in problem:
                additional_test_cases_generator = fetch_test_cases(problem["uva_id"])

            zipper = Zipper(problem, output_path, pdf_path, additional_test_cases_generator)
            zipped_file_path = zipper.zip()
            print("Problem generated and saved in: " + zipped_file_path)
if __name__ == "__main__":
    fire.Fire(QGen)