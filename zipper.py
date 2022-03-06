import zipfile
import os
from tempfile import NamedTemporaryFile

class Zipper:
    """
        The Zipper class will produce a zipped problem data with the proper format.
        Inputs: template, problem_pdf_path
        Output: zipped_file_path
    """

    def __init__(self, template, output_path, problem_pdf_path):
        self.template = template
        self.output_path = output_path
        self.problem_pdf_path = problem_pdf_path
        self.ini_file_name = None
    
    def get_ini_file_contents(self):
        lines = [
            "title=" + self.template.title,
            "short_name=" + self.template.short_name,
            "time_limit=" + str(self.template.time_limit),
            "ballon_color=" + self.template.ballon_color
        ]
        return "\n".join(lines)
    
    def get_ini_file(self):
        if self.ini_file_name:
            return self.ini_file_name
        ini_file_contents = self.get_ini_file_contents()
        ini_file = NamedTemporaryFile(delete=False)
        ini_file.write(ini_file_contents.encode())
        ini_file.close()
        self.ini_file_name = ini_file.name
        return self.ini_file_name

    def zip(self):
        output_file_name = self.template.name + ".zip"
        output_file_path = os.path.join(self.output_path, output_file_name)
        with zipfile.ZipFile(output_file_path, "w") as zip_file:
            zip_file.write(self.problem_pdf_path, arcname="problem.pdf")
            zip_file.write(self.get_ini_file(), arcname="info.ini")
            io_filename_letter_index = 0
            for input_file, output_file in self.template.files.items():
                io_filename_letter = chr(ord('a') + io_filename_letter_index)
                zip_file.write(input_file, arcname=io_filename_letter + ".in")
                zip_file.write(output_file, arcname=io_filename_letter + ".out")
                io_filename_letter_index += 1
        return output_file_path
