import json
import os
import tempfile
import shutil
import zipfile

from lark import Lark, Tree

class ScratchProject():

    def __init__(self, filename):
        self.CUR_ID = 0
        self.variables = dict()
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(tmpdir)
        with open(os.path.join(tmpdir, "project.json")) as f:
            self.data = json.loads(f.read())
        self.origin = filename
        shutil.rmtree(tmpdir)

    def generate_id(self, arg=None):
        self.CUR_ID += 1
        if arg:
            return f"scratchtext-{arg}-{self.CUR_ID}"
        else:
            return f"scratchtext-{self.CUR_ID}"

    def variable(self, name):
        if name not in self.variables:
            self.variables[name] = self.generate_id(arg="var")
        return self.variables[name]

    def generate_block(self, statement):
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

        elif opcode == "event_whenthisspriteclicked":
            pass

        elif opcode == "event_whenkeypressed":
            block["fields"] = statement["data"]["fields"]

        # Motion
        elif opcode == "motion_movesteps":
            block["inputs"] = {
                "STEPS": [
                    1,
                    [4, str(statement["text_value"])]
                ]
            }

        elif opcode == "motion_gotoxy":
            block["inputs"] = {
                "X": [
                    1, [4, str(statement["x"])]
                ],
                "Y": [
                    1, [4, str(statement["y"])]
                ]
            }

        # Turn right
        elif opcode == "motion_turnright":
            block["inputs"] = {
                "DEGREES": [
                    1,
                    [4, str(statement["text_value"])]
                ]
            }
        
        elif opcode == "motion_glidesecstoxy":
            block["inputs"] = {
                "SECS": [1, [4, str(statement["secs"])]],
                "X": [1, [4, str(statement["x"])]],
                "Y": [1, [4, str(statement["y"])]]
            }
        elif opcode == "motion_setx":
            block["inputs"] = {
                "X": [1, [4, str(statement["x"])]]
            }
        elif opcode == "motion_sety":
            block["inputs"] = {
                "Y": [1, [4, str(statement["y"])]]
            }

        # Looks
        elif opcode == "looks_think":
            block["inputs"] = {
                "MESSAGE": [
                    1,
                    [10, statement["argument"]]
                ]
            }
        elif opcode == "looks_say":
            block["inputs"] = {
                "MESSAGE": [
                    1,
                    [10, statement["argument"]]
                ]
            }
        elif opcode == "looks_show":
            pass
        elif opcode == "looks_hide":
            pass

        # Control
        # Condition
        elif opcode == "control_repeat":
            block["inputs"] = {
                "TIMES": [
                    1,
                    [6, str(statement["argument"])]
                ]
            }
        
        elif opcode == "control_wait":
            block["inputs"] = {
                "DURATION": [1, [5, str(statement["argument"])]]
            }

        # Variables
        elif opcode == "data_setvariableto":
            variable = statement["variable"]
            value = statement["value"]
            variable_id = self.variable(variable)
            block["inputs"] = {
                "VALUE": [
                    1, [10, value]
                ]
            }
            block["fields"] = {
                "VARIABLE": [variable, variable_id]
            }

        return block

    def add_program(self, program):
        for sprite in program:
            for target in self.data["targets"]:
                if target["name"] == sprite:
                    self.add_sprite_scripts(target, program[sprite])
        
        # Add variables
        for target in self.data["targets"]:
            if target["isStage"]:
                if "variables" not in target:
                    target["variables"] = dict()
                for variable in self.variables:
                    variable_id = self.variables[variable]
                    target["variables"][variable_id] = [variable, "0"]

    def add_sprite_scripts(self, target, program):
        script_count = 0
        print("adding program", program)
        self.variables = dict()
        for script in program:
            self.add_block(target, script, prev=None, script_offset=script_count)
            script_count += 1

    def add_block(self, target, block, prev=None, script_offset=0, first_child=False):
        print("adding block", block)
        block_id = self.generate_id()
        scratch_block = self.generate_block(block)

        if prev is None:
            scratch_block["topLevel"] = True
            scratch_block["x"] = 50 + (script_offset * 300)
            scratch_block["y"] = 50
        else:
            prev_block = target["blocks"][prev]
            if not first_child:
                prev_block["next"] = block_id
            else:
                if "inputs" not in prev_block:
                    prev_block["inputs"] = dict()
                prev_block["inputs"]["SUBSTACK"] = [2, block_id]
            scratch_block["parent"] = prev

        target["blocks"][block_id] = scratch_block

        cprev = block_id # previous id as we iterate through body of a function
        for child in block.get("body", []):
            cprev = self.add_block(target, child, prev=cprev, script_offset=script_offset)

        first = True
        for child in block.get("children", []):
            cprev = self.add_block(target, child, prev=cprev, script_offset=script_offset, first_child=first)
            first = False
        
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
        data = dict()
        if func == "when_flag_clicked":
            opcode = "event_whenflagclicked"
        elif func == "when_clicked":
            opcode = "event_whenthisspriteclicked"
        elif func == "when_space_pressed":
            opcode = "event_whenkeypressed"
            data = {
                "fields": {"KEY_OPTION": ["space", None]}
            }
        operations = [parse_tree(c) for c in t.children[1:]]
        return {
            "opcode": opcode,
            "body": operations,
            "data": data
        }

    print(t)
    if t.data == "instruction":

        if isinstance(t.children[0], Tree):
            root = t.children[0]
            data = root.data
            if data == "assignment":
                variable = str(root.children[0])
                value = str(root.children[1])
                return {
                        "opcode": "data_setvariableto",
                        "variable": variable,
                        "value": value
                }
            
            return None

        instr_type = t.children[0].type
        func = str(t.children[0])

        # Control
        if func == "forever":
            return {
                "opcode": "control_forever",
                "children": [parse_tree(child) for child in t.children[1:]]
            }
        elif func == "repeat":
            return {
                "opcode": "control_repeat",
                "argument": str(t.children[1]),
                "children": [parse_tree(child) for child in t.children[2:]]
            }
        elif func == "wait":
            return {
                "opcode": "control_wait",
                "argument": str(t.children[1])
            }

        # Motion
        elif func == "move":
            return {
                "opcode": "motion_movesteps",
                "text_value": str(t.children[1])
            }
        elif func == "turn":
            return {
                "opcode": "motion_turnright",
                "text_value": str(t.children[1])
            }
        elif func == "goto" and instr_type == "BINFUNC":
            return {
                "opcode": "motion_gotoxy",
                "x": str(t.children[1]),
                "y": str(t.children[2])
            }
        elif func == "glide" and instr_type == "TRIFUNC":
            return {
                "opcode": "motion_glidesecstoxy",
                "secs": str(t.children[1]),
                "x": str(t.children[2]),
                "y": str(t.children[3])
            }
        elif func == "setX":
            return {
                "opcode": "motion_setx",
                "x": str(t.children[1])
            }
        elif func == "setY":
            return {
                "opcode": "motion_sety",
                "y": str(t.children[1])
            }
        
        # Looks
        elif func == "think":
            return {
                "opcode": "looks_think",
                "argument": str(t.children[1].value)[1:-1]
            }
        elif func == "say":
            return {
                "opcode": "looks_say",
                "argument": str(t.children[1].value)[1:-1]
            }
        elif func == "show":
            return {
                "opcode": "looks_show"
            }
        elif func == "hide":
            return {
                "opcode": "looks_hide"
            }

    return None

