from flask import Flask, request, jsonify
from evaluators import evaluate_resources
from datetime import datetime

app = Flask(__name__)

MAX_REQUEST_SIZE = 100 * 1024  # 100 KB


@app.before_request
def basic_security():
    if request.content_length and request.content_length > MAX_REQUEST_SIZE:
        return jsonify({"error": "Request too large"}), 413

    if request.method == "POST" and not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/v1/evaluate", methods=["POST"])
def evaluate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty JSON body"}), 400

        results = evaluate_resources(data)

        response = {
            "metadata": {
                "evaluated_at": datetime.utcnow().isoformat(),
                "resource_count": {
                    key: len(value) for key, value in results.items()
                }
            },
            "results": results
        }

        return jsonify(response), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception:
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("Starting Flask server")
    app.run(debug=True)
