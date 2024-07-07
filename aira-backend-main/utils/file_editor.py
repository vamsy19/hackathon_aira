from .base import BaseTool
import os


class FileEditor(BaseTool):
    def __init__(self, config={}):
        self.root_folder = config.get("working_directory", '.')

    def on_input_received(self, msg):
        command = msg['data']
        if "write_to_file" in command:
            self.write_to_file(command["write_to_file"], command["contents"])
        else:
            raise ValueError("Invalid command")

        reply = {}
        reply['metadata'] = {"status": "success"}
        reply['data'] = {"message": "File updated successfully"}
        return reply

    def write_to_file(self, filepath, contents):
        full_path = os.path.join(self.root_folder, filepath)
        with open(full_path, 'w') as file:
            file.write(contents)
