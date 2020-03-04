import json
import os
import tempfile
import shutil
import zipfile

from lark import Lark

class ScratchProject():

    CUR_ID = 0

    def __init__(self, filename):
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(tmpdir)
        with open(os.path.join(tmpdir, "project.json")) as f:
            self.data = json.loads(f.read())
        self.origin = filename
        shutil.rmtree(tmpdir)

    @classmethod
    def generate_id(cls):
        ScratchProject.CUR_ID += 1
        return f"scratchtext-{ScratchProject.CUR_ID}"

    @classmethod
    def generate_block(cls, statement):
        opcode = statement["opcode"]

        block = {
            "opcode": opcode,
            "parent": None,
            "next": None,
            "inputs": {},
            "fields": {},
            "shadow": False,
            "topLevel": False,
            "x": 0,
            "y": 0
        }

        # Events
        if opcode == "event_whenflagclicked":
            pass

        # Motion
        elif opcode == "motion_movesteps":
            block["inputs"] = {
                "STEPS": [
                    1,
                    [4, str(statement["text_value"])]
                ]
            }

        return block

    def add_program(self, program):
        for sprite in program:
            for target in self.data["targets"]:
                if target["name"] == sprite:
                    self.add_sprite_scripts(target, program[sprite])

    def add_sprite_scripts(self, target, program):
        script_count = 0
        print("adding program", program)
        for script in program:
            self.add_block(target, script, prev=None, script_offset=script_count)
            script_count += 1

    
    def add_block(self, target, block, prev=None, script_offset=0):
        print("adding block", block)
        block_id = ScratchProject.generate_id()
        scratch_block = ScratchProject.generate_block(block)

        if prev is None:
            scratch_block["topLevel"] = True
            scratch_block["x"] = 50
            scratch_block["y"] = 50 + (script_offset * 30)
        else:
            target["blocks"][prev]["next"] = block_id
            scratch_block["parent"] = prev

        target["blocks"][block_id] = scratch_block

        cprev = block_id # previous id as we iterate through children
        for child in block.get("children", []):
            cprev = self.add_block(target, child, prev=cprev, script_offset=script_offset)
            
        return block_id


    def write(self, filename):

        # Load old contents
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(self.origin, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        # Replace project.json
        with open(os.path.join(tmpdir, "project.json"), "w") as f:
            f.write(json.dumps(self.data))

        zip_ref = zipfile.ZipFile(filename, "w")
        for content_file in os.listdir(tmpdir):
            zip_ref.write(os.path.join(tmpdir, content_file), arcname=content_file)
        zip_ref.close()
        shutil.rmtree(tmpdir)


with open("scratch.lark") as f:
    ScratchParser = Lark(f.read())

def parse(text):
    return parse_tree(ScratchParser.parse(text))

def parse_tree(t):
    if t.data == "start":
        return list(map(parse_tree, t.children))

    if t.data == "function_definition":
        func = str(t.children[0])
        opcode = "none"
        if func == "when_flag_clicked":
            opcode = "event_whenflagclicked"
        operations = [parse_tree(c) for c in t.children[1:]]
        return {
            "opcode": opcode,
            "children": operations
        }

    if t.data == "instruction":
        func = str(t.children[0])
        arg = str(t.children[1])
        if func == "move":
            return {
                "opcode": "motion_movesteps",
                "text_value": arg
            }

    return None

