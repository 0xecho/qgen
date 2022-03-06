import shutil
from tempfile import NamedTemporaryFile
from docxtpl import DocxTemplate
import subprocess

class Generator:
    def __init__(self, problem, format_file):
        self.problem = problem
        self.format_file = format_file
    
    def get_output_path(self, suffix=".docx"):
        temporary_file = NamedTemporaryFile(delete=False, suffix=suffix)
        return temporary_file.name

    def generate(self):
        doc = DocxTemplate(self.format_file)
        context = {
            "problem_title": self.problem["title"],
            "time_limit": self.problem["time_limit"],
            "balloon_color": self.problem["balloon_color"],
            "body": self.problem["body"],
            "input_description": self.problem["input"]["description"],
            "output_description": self.problem["output"]["description"],
            "samples": self.problem["samples"]
        }
        doc.render(context)
        output_path = self.get_output_path()
        doc.save(output_path)
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", output_path])
        current_pdf_path = output_path.split(".")[0].split("/")[-1] + ".pdf"
        pdf_output_path = self.get_output_path(suffix=".pdf")
        shutil.move(current_pdf_path, pdf_output_path)
        return pdf_output_path
        
        

    