import os
import sys
from uuid import uuid4

from chat import ask_question
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)


@app.route("/")
def api_index():
    return app.send_static_file("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    request_json = request.get_json()
    question = request_json.get("question")
    if question is None:
        return jsonify({"msg": "Missing question from request JSON"}), 400

    session_id = request.args.get("session_id", str(uuid4()))
    return Response(ask_question(question, session_id), mimetype="text/event-stream")


@app.cli.command()
def create_index():
    """Create or re-create the Elasticsearch index."""
    basedir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(f"{basedir}/../")

    from data import index_data

    index_data.main()


# Unless we run through flask, we can miss critical settings or telemetry signals.
if __name__ == "__main__":
    raise RuntimeError("Run via the parent directory: 'flask run'")
