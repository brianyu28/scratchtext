import os
import json
import scratch
import shutil
import tempfile

from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    program = json.loads(request.form["scripts"])
    f = request.files["file"]

    # Save old file
    tmpdir = tempfile.mkdtemp()
    print(tmpdir)
    f.save(os.path.join(tmpdir, "old.sb3"))

    # Parse new program
    program = {sprite : scratch.parse(program[sprite])
               for sprite in program}
    project = scratch.ScratchProject(os.path.join(tmpdir, "old.sb3"))
    project.add_program(program)
    project.write(os.path.join(tmpdir, "new.sb3"))
    return send_file(os.path.join(tmpdir, "new.sb3"))
