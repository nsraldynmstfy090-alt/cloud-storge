from flask import Flask, request, jsonify
import subprocess, uuid, os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def run_cpp():
    code = request.json["code"]

    file_id = str(uuid.uuid4())
    cpp_file = f"/tmp/{file_id}.cpp"
    exe_file = f"/tmp/{file_id}.out"

    with open(cpp_file, "w") as f:
        f.write(code)

    try:
        subprocess.run(
            ["g++", cpp_file, "-o", exe_file],
            check=True,
            stderr=subprocess.STDOUT
        )

        output = subprocess.check_output(
            [exe_file], stderr=subprocess.STDOUT
        ).decode()

    except subprocess.CalledProcessError as e:
        output = e.output.decode() if e.output else str(e)

    return jsonify({"output": output})
