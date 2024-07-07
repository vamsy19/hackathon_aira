from utils.coder import Coder
config = {
    "working_directory": "/home/tarun/Workspace/Naulets2/NauletsV2-Backend/courses"}
coder = Coder(config)
res = coder.modify_file('admin.py', 'refactor the code')
