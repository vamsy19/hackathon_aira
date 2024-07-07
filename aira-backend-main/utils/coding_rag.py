import traceback
from .base import BaseTool
import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
import chromadb
from langchain_chroma import Chroma


class CodingRAG(BaseTool):
    def __init__(self, config):
        self.root_folder = config.get("working_directory")

    def index_file(self, filepath):
        full_path = os.path.join(self.root_folder, filepath)
        with open(full_path, 'r') as file:
            contents = file.read()
            python_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON, chunk_size=10000, chunk_overlap=0)
            python_docs = python_splitter.create_documents([contents])

            # add metadata
            for doc in python_docs:
                doc.metadata['filepath'] = filepath
            return python_docs

    def index_all(self):
        all_docs = []
        for dirpath, _, filenames in os.walk(self.root_folder):
            for filename in filenames:
                if filename.endswith('.py'):
                    filepath = os.path.join(dirpath, filename)
                    docs = self.index_file(filepath)
                    all_docs.extend(docs)
        return all_docs

    def get_relevant_files(self, query):
        docs = self.index_all()
        if not docs:
            return []
        embedding_function = OpenAIEmbeddings(
            model="text-embedding-3-large", openai_api_key='sk-proj-M5JGu510Q8qf8Bs4zfZmT3BlbkFJWo3REvFQUoRrs3aOYeGG')
        db = Chroma.from_documents(docs, embedding_function)
        docs = db.similarity_search(query)
        filepaths = set()
        for doc in docs:
            relative_path = os.path.relpath(
                doc.metadata['filepath'], self.root_folder)
            filepaths.add(relative_path)
        return list(filepaths)

    def on_input_received(self, msg):
        command = msg['data']
        if "get_relevant" in command:
            try:
                files = self.get_relevant_files(command['get_relevant'])
                reply = {}
                reply['metadata'] = {"status": "success"}
                reply['data'] = {"relevant_files": files}
            except Exception as e:
                print(traceback.format_exc())
                reply = {}
                reply['metadata'] = {"status": "failed",
                                     "error": "something went wrong, try again"}
                reply['data'] = {}
        else:
            reply = {}
            reply['metadata'] = {"status": "failed",
                                 "error": "command not found"}
            reply['data'] = {}
        return reply
