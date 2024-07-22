# Import flask
from flask import Flask, request, jsonify
from settings import settings


app = Flask(__name__)

# Route with dynamic parameter
@app.route("/settings/<string:section>", methods=["GET"])
def get_setting(section):
    if section in settings:
        return jsonify(settings[section])
    else:
        return jsonify({"error": "Setting not found"}), 404
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)