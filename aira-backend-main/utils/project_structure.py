import os
import shutil
import json
from .base import BaseTool


class ProjectStructure(BaseTool):
    def __init__(self, config={}):
        # print(config)
        self.root_folder = config.get("working_directory", '.')
        self.project_structure = {}
        self.expanded_folders = []

    def on_input_received(self, msg):
        command = msg['data']
        try:

            if("get_structure") in command:
                print("getting project structure")
            elif "expand" in command:
                self.expand(command["expand"])
            elif "condense" in command:
                self.condense(command["condense"])
            elif "create_folder" in command:
                self.create_folder(command["create_folder"])
            elif "create_file" in command:
                self.create_file(command["create_file"])
            elif "move_folder" in command:
                self.move_folder(command["move_folder"], command["new_location"])
            elif "move_file" in command:
                self.move_file(command["move_file"], command["new_location"])
            elif "copy_folder" in command:
                self.copy_folder(command["copy_folder"], command["new_location"])
            elif "copy_file" in command:
                self.copy_file(command["copy_file"], command["new_location"])
            elif "delete_folder" in command:
                self.delete_folder(command["delete_folder"])
            elif "delete_file" in command:
                self.delete_file(command["delete_file"])
            else:
                reply = {}
                reply['metadata'] = {"status": "failed",
                                    "error": "Invalid command"}
                reply['data'] = {}
                return reply
        except Exception as e:
            reply = {}
            reply['metadata'] = {"status": "failed",
                                "error": str(e)}
            reply['data'] = {}
            return reply

        # calculate new folder structure
        self.evaluate_project_structure()
        reply = {}
        reply['metadata'] = {"status": "success"}
        reply['data'] = {"project_structure": self.project_structure}
        return reply

    def expand(self, path):
        full_path = os.path.join(self.root_folder, path)
        self.expanded_folders.append(full_path)

    def condense(self, path):
        if path in self.expanded_folders:
            self.expanded_folders.remove(path)

    def create_folder(self, path):
        full_path = os.path.join(self.root_folder, path)
        os.makedirs(full_path, exist_ok=True)

    def create_file(self, path):
        full_path = os.path.join(self.root_folder, path)
        with open(full_path, 'w') as f:
            pass

    def move_folder(self, folder_path, new_location):
        full_folder_path = os.path.join(self.root_folder, folder_path)
        full_new_location = os.path.join(self.root_folder, new_location)
        shutil.move(full_folder_path, full_new_location)

    def move_file(self, file_path, new_location):
        full_file_path = os.path.join(self.root_folder, file_path)
        full_new_location = os.path.join(self.root_folder, new_location)
        shutil.move(full_file_path, full_new_location)

    def copy_folder(self, folder_path, new_location):
        full_folder_path = os.path.join(self.root_folder, folder_path)
        full_new_location = os.path.join(self.root_folder, new_location)
        shutil.copytree(full_folder_path, full_new_location)

    def copy_file(self, file_path, new_location):
        full_file_path = os.path.join(self.root_folder, file_path)
        full_new_location = os.path.join(self.root_folder, new_location)
        shutil.copy2(full_file_path, full_new_location)

    def delete_folder(self, folder_path):
        full_folder_path = os.path.join(self.root_folder, folder_path)
        shutil.rmtree(full_folder_path)

    def delete_file(self, file_path):
        full_file_path = os.path.join(self.root_folder, file_path)
        os.remove(full_file_path)

    def get_folder_structure(self, path):
        project_structure = {"folders": [], "files": []}
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                if full_path in self.expanded_folders:
                    project_structure["folders"].append(
                        {"name": item, "contents": self.get_folder_structure(full_path)})
                else:
                    num_items = len(os.listdir(full_path))
                    project_structure["folders"].append(
                        {"name": item, "num_items": num_items})
            elif os.path.isfile(full_path):
                project_structure["files"].append(item)
        return project_structure

    def evaluate_project_structure(self):
        self.project_structure = self.get_folder_structure(self.root_folder)
