from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

# 🔐 Uzum API key (keep in Vercel env vars for safety)
UZUM_KEY = os.getenv("UZUM_KEY", "EPZsaV5uKvCXbDEmjDf2a7uHcX4vDG/rYK8WBcaFGhU=")

BASE_URL = "https://api-seller.uzum.uz/api/seller-openapi"

@app.route("/uzum/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(endpoint):
    """
    Universal proxy for Uzum Seller API.
    Example: https://yourapp.vercel.app/uzum/v1/fbs/orders
    """
    # ✅ Corrected indentation
    if endpoint.startswith("api/"):
        endpoint = endpoint.replace("api/", "", 1)

    target = f"{BASE_URL}/{endpoint}"

    headers = {
        "Authorization": UZUM_KEY,
        "Content-Type": "application/json"
    }

    try:
        if request.method == "GET":
            resp = requests.get(target, headers=headers, params=request.args)
        elif request.method == "POST":
            resp = requests.post(target, headers=headers, json=request.get_json(silent=True))
        elif request.method == "PUT":
            resp = requests.put(target, headers=headers, json=request.get_json(silent=True))
        elif request.method == "DELETE":
            resp = requests.delete(target, headers=headers, json=request.get_json(silent=True))
        else:
            return jsonify({"error": "Unsupported method"}), 405

        return (resp.text, resp.status_code, {"Content-Type": resp.headers.get("Content-Type", "application/json")})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Required for Vercel entrypoint
def handler(event, context):
    return app(event, context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
