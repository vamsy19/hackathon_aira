import json


class BaseTool():
    def __init__(self, config={}):
        pass

    def on_input_received(self, input):
        raise NotImplementedError("Subclasses should implement this method")

    def serialize(self):
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        instance_data = json.loads(data)
        for key, value in instance_data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def required_fields(cls):
        # Return a list of fields that need to be serialized
        return []
