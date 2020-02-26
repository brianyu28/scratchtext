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

project = scratch.ScratchProject("old.sb3")
project.add_program(program)

project.write("new.sb3")
