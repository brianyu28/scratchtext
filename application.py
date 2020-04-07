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
    try:
        f = request.files["file"]
    except KeyError:
        f = None

    tmpdir = tempfile.mkdtemp()

    # Log tmpdir
    with open("log.txt", "a") as log:
        log.write(tmpdir)
        log.write("\n")

    # Save old file
    if f is not None:
        f.save(os.path.join(tmpdir, "old.sb3"))
    else:
        shutil.copyfile(
            os.path.join("assets", "start.sb3"),
            os.path.join(tmpdir, "old.sb3")
        )

    # Parse new program
    program = {sprite : scratch.parse(program[sprite])
               for sprite in program}
    project = scratch.ScratchProject(os.path.join(tmpdir, "old.sb3"))
    project.add_program(program)
    project.write(os.path.join(tmpdir, "new.sb3"))
    return send_file(os.path.join(tmpdir, "new.sb3"))
