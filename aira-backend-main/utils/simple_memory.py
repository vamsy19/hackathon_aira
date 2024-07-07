from .base import BaseTool

class SimpleMemory(BaseTool):
    def __init__(self, config={}):
        self.memory = []

    def on_input_received(self, msg):
        data = msg['data']
        if 'add_to_memory' in data:
            self.add_to_memory(data['add_to_memory'])
            reply = {
                'metadata': {"status": "success"},
                'data': {"message": "Data added to memory successfully"}
            }
        elif 'get_data_from_memory' in data:
            memory_data = self.get_memory()
            reply = {
                'metadata': {"status": "success"},
                'data': {"memory": memory_data}
            }
        else:
            reply = {
                'metadata': {"status": "error"},
                'data': {"message": "Invalid input format"}
            }
        return reply

    def add_to_memory(self, data):
        self.memory.append(data)

    def get_memory(self):
        return self.memory

    def clear_memory(self):
        self.memory = []

    @classmethod
    def required_fields(cls):
        return ['memory']
