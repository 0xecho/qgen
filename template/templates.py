import json
from schema import Schema, And, Use, Optional

class Template:
    def __init__(self, template_path):
        self.template_path = template_path
        self.template_data = self.read_template()
        self.schema = Schema({
            "questions": [
                {
                    "title": And(str, len),
                    "short_title": And(str, len),
                    "time_limit": And(int, lambda n: n > 0),
                    Optional("uva_id"): And(int, lambda n: n > 0),
                    "balloon_color": And(str, len),
                    "body": And(list, len),
                    "input": {
                        "description": And(str, len),
                    },
                    "output": {
                        "description": And(str, len),
                    },
                    "samples": [
                        {
                            "input": And(list, len),
                            "output": And(list, len)
                        }
                    ],
                    "testcases": {
                            "input_paths": And(list, lambda l: all(map(lambda s: s.endswith("in"), l))),
                            "output_paths": And(list, lambda l: all(map(lambda s: s.endswith("out"), l))),
                        }
                }
            ]
        })

        self.data = self.get_validated_data()
        self.files = self.get_files()
    
    def read_template(self):
        with open(self.template_path, "r") as template_file:
            template_data = json.load(template_file)
        return template_data

    def get_validated_data(self):
        validated_data = self.schema.validate(self.template_data)
        for question in validated_data["questions"]:
            self.check_if_input_output_names_match(question)
        return validated_data
    
    def check_if_input_output_names_match(self, question):
        input_paths = question["testcases"]["input_paths"]
        output_paths = question["testcases"]["output_paths"]
        input_paths_before_dot = map(lambda file_name: file_name.split(".")[0], input_paths)
        output_paths_before_dot = map(lambda file_name: file_name.split(".")[0], output_paths)
        assert sorted(input_paths_before_dot) == sorted(output_paths_before_dot), "Input and Output files mismatched"        
    
    def get_files_for_question(self, question):
        input_output_map = dict()
        input_files = question["testcases"]["input_paths"]
        output_files = question["testcases"]["output_paths"]
        for input_file, output_file in zip(sorted(input_files), sorted(output_files)):
            input_output_map[input_file] = output_file
        return input_output_map
    
    def get_files(self):
        files = dict()
        for question in self.data["questions"]:
            files[question["short_title"]] = self.get_files_for_question(question)
        return files
    
    def get_problems(self):
        return self.data["questions"]