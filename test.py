import scratch

program = {
    "S1": [
        [
            {"opcode": "event_whenflagclicked"},
            {"opcode": "motion_movesteps", "text_value": 28},
            {"opcode": "motion_movesteps", "text_value": 10},
        ]
    ]
}

src = """
when_flag_clicked() {
    move(10)
    move(10)
}
"""

program = {"S1": scratch.parse(src)}
print(program)

project = scratch.ScratchProject("old.sb3")
project.add_program(program)
project.write("new.sb3")