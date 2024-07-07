from .base import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import json
import os


class Coder(BaseTool):
    def __init__(self, config={}):
        self.root_folder = config.get("working_directory")
        self.system_prompt = """
You are an intelligent programmer. You are happy to help with modifying the code given by the user, based on his instructions.
Important instructions:
1. Rewrite the code provided by user according to the instructions. 
2. Include the complete code in your response.
3. Your response should only contain code. 
4. Feel free to add comments. 
5. Use best practices. """
        chat = ChatOpenAI(
            model="gpt-4o", api_key='sk-proj-M5JGu510Q8qf8Bs4zfZmT3BlbkFJWo3REvFQUoRrs3aOYeGG')
        self.chain = chat | StrOutputParser()
        # self.chain = chat

    def modify_file(self, filepath, instructions):
        full_path = os.path.join(self.root_folder, filepath)
        with open(full_path, 'r') as file:
            contents = file.read()
            messages = [
                SystemMessage(
                    content=self.system_prompt),
                HumanMessage(content=instructions),
                HumanMessage(content=contents)
            ]
            response = self.chain.invoke(messages)
            start_index = response.find("```python") + len("```python")
            end_index = response.find("```", start_index)
            if start_index != -1 and end_index != -1:
                response = response[start_index:end_index].strip()

            with open(full_path, 'w') as file:
                file.write(response)

    def modify_files(self, filepaths, instructions):
        for filepath in filepaths:
            self.modify_file(filepath, instructions)

    def on_input_received(self, msg):
        try:
            command = msg['data']
            if "modify_file" in command:
                self.modify_file(command["modify_file"],
                                 command["instructions"])
                reply = {
                    'metadata': {"status": "success"},
                    'data': {"message": "File modified successfully"}
                }
            elif "modify_files" in command:
                self.modify_files(
                    command["modify_files"], command["instructions"])
                reply = {
                    'metadata': {"status": "success"},
                    'data': {"message": "Files modified successfully"}
                }
            else:
                reply = {
                    'metadata': {"status": "failed", "error": "Invalid command"},
                    'data': {}
                }
        except Exception as e:
            reply = {
                'metadata': {"status": "failed", "error": str(e)},
                'data': {}
            }
        return reply
