from .models import *
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import json
import copy


class NodeLLM():
    def __init__(self, node, orchestra):
        self.orchestra = orchestra
        self.node = node
        system_prompt = node.get_full_prompt()
        chat = ChatOpenAI(
            model="gpt-4o", api_key='sk-proj-M5JGu510Q8qf8Bs4zfZmT3BlbkFJWo3REvFQUoRrs3aOYeGG',temperature=0)
        self.chain = chat | JsonOutputParser()
        self.messages = [
            SystemMessage(
                content=system_prompt),
        ]

    def next_message(self, msg):
        try:
            self.messages.append(HumanMessage(content=json.dumps(msg)))
            response = self.chain.invoke(self.messages)
            self.messages.append(AIMessage(content=json.dumps(response)))

            reply = {}
            reply['metadata'] = {}
            reply['data'] = {}
            if response['to'] == 'user':
                if self.orchestra.get_user_agent(self.node) is None:
                    reply['metadata']['to'] = response['to']
                else:
                    reply['metadata']['to'] = self.orchestra.get_user_agent(
                        self.node)
            else:
                reply['metadata']['to'] = response['to']
            reply['metadata']['from'] = self.node.name
            reply['data'] = response['msg']
            return reply

        except Exception as e:
            msg = {}
            msg['metadata'] = {
                'status': "Failed", "error_msg": "Sending your last message failed, please try again. Make sure json format is used"}
            return self.next_message(msg)


class NodeRunner():

    def __init__(self, node, orchestra):
        self.node = node
        if node.tool_instance:
            self.runner = node.tool_instance.get_tool_instance()
        elif node.entry_node:
            self.runner = Orchestra(self.node.entry_node)
        else:
            self.runner = NodeLLM(node, orchestra)

    def respond_to_message(self, msg):
        if self.node.tool_instance:
            reply = self.runner.on_input_received(msg)
            reply['metadata']['to'] = msg['metadata']['from']
            reply['metadata']['from'] = msg['metadata']['to']
            return reply
        elif self.node.entry_node:
            asked = msg['metadata']['from']
            # print("#############")
            # print(asked)
            # print(msg['metadata']['from'])
            new_msg = copy.deepcopy(msg)
            new_msg['metadata']['from'] = "user"
            new_msg['metadata']['to'] = self.node.entry_node.name

            reply = self.runner.run(new_msg)
            
            reply['metadata']['to'] = msg['metadata']['from']
            reply['metadata']['from'] = self.node.name
            
            # print("@@@@@@@@@@@")
            # print(asked)
            # print(msg['metadata']['from'])
            return reply
        else:
            reply = self.runner.next_message(msg)
            return reply


class Orchestra():
    def __init__(self, node):
        self.entry_node = node
        self.nodes = [node]
        self.get_connected_nodes(node)
        self.node_runners = []

        for node in self.nodes:
            nr = NodeRunner(node, self)
            self.node_runners.append(nr)
            if node == self.entry_node:
                self.entry_runner = nr

    def get_connected_nodes(self, node):
        edges = Edge.objects.filter(source=node)
        for edge in edges:
            if edge.target not in self.nodes:
                self.nodes.append(edge.target)
                self.get_connected_nodes(edge.target)

    def send_message(self, msg):
        if(msg['metadata']['to']==msg['metadata']['from']):
            reply = {}
            reply['metadata']={"to":msg['metadata']['to'],"from":"system", "status": "failed","error":"Can't send message to self."}
            reply['data']={}
            return reply

        for noderunner in self.node_runners:
            if noderunner.node.name == msg['metadata']['to']:
                return noderunner.respond_to_message(msg)
        # reply back saying no node with that name
        reply = {}
        reply['metadata']={"to":msg['metadata']['from'],"from":"system", "status": "failed","error":"Agent or tool not found"}
        reply['data']={}
        return reply

    def get_user_agent(self, node):
        if self.entry_node == node:
            return None
        else:
            user_agent = node.target_edges.filter(
                source__in=self.nodes).first().source
            return user_agent.name

    def respond_to_message(self, msg):
        while msg and msg['metadata']['to'] != 'user':
            print(msg)
            msg = self.send_message(msg)
        print(msg)
        return msg

    def run(self, msg):
        while msg and msg['metadata']['to'] != 'user':
            print(msg)
            msg = self.send_message(msg)
        print(msg)
        return msg
