import os
import pty
import subprocess
from .base import BaseTool
import json
import re
import time

class Terminal(BaseTool):

    def __init__(self, config={}):
        self.master_fd, self.slave_fd = pty.openpty()

        # Use the working directory from config if provided
        working_directory = config.get("working_directory", None)

        self.process = subprocess.Popen(
            ['/bin/bash'],
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            cwd=working_directory,  # Set the working directory
            close_fds=True,
            preexec_fn=os.setsid,
        )
        self.history = []
        self.prompt = self._initialize_prompt()

    def _initialize_prompt(self):
        output = b''
        while True:
            try:
                data = os.read(self.master_fd, 1024)
                output += data
                if data.endswith(b'$ ') or data.endswith(b'# '):
                    break
            except OSError:
                break

        output_str = output.decode()
        lines = output_str.split('\r\n')
        prompt = lines[-1].strip()
        return prompt

    def run_command(self, command, timeout=30):
        os.write(self.master_fd, (command + '\n').encode())

        output = b''
        while True:
            try:
                data = os.read(self.master_fd, 1024)
                output += data
                # Check for common prompts or cursor-related escape sequences
                if data.endswith(b'$ ') or data.endswith(b'# '):
                    break
            except OSError:
                break
        output_str = output.decode()
        lines = output_str.split('\r\n')
        cleaned_output = '\n'.join(line for line in lines[1:] if line).strip()

        self.history.append((f"{self.prompt} {command}", cleaned_output))
        self.prompt = lines[-1].strip()

    def get_history(self):
        return self.history

    def close(self):
        os.close(self.master_fd)
        os.close(self.slave_fd)
        self.process.terminate()

    def clean_terminal_output(self, raw_output):
        # Regex to remove escape sequences
        clean_output = re.sub(r'\x1b\[.*?[@-~]', '', raw_output)
        clean_output = re.sub(r'\x1b\].*?\x07', '', clean_output)
        clean_output = re.sub(r'\x1b\[\?2004[hl]', '', clean_output)

        # Remove any additional carriage returns or newlines at the end of the string
        clean_output = clean_output.strip()

        return clean_output

    def print_history(self):
        for command, output in self.history:
            print(f"{command}\n{output}")

    def on_input_received(self, msg):
        data = msg['data']

        self.run_command(data['command'])
        # self.print_history()
        output_data = ''
        for command, output in self.history:
            # print(f"{command}\n{output}")
            output_data += f"{command}\n{output}\n"

        od = '\n'.join(output_data.split('\n')[-2:-1])

        reply = {}
        reply['metadata'] = {"status": "success"}
        reply['data'] = {
            "terminal_output": self.clean_terminal_output(od)}
        return reply

    @classmethod
    def required_fields(cls):
        return ['history']
