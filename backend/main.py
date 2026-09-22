
from flask import Flask, request, jsonify
from mysql.connector import Error

import mission_manager


app = Flask(__name__)


# Home endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to FLEETOS Backend",
        "status": "Running"
    })


# Create a new mission
@app.route("/missions", methods=["POST"])
def add_mission():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON request body is required"}), 400

    required_fields = [
        "mission_type",
        "priority",
        "location"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": field + " is required"
            }), 400

    try:
        result = mission_manager.create_mission(data)

        return jsonify(result), 201

    except Error:
        app.logger.exception("Database error while creating mission")
        return jsonify({
            "error": "Could not create mission"
        }), 500


# Get all missions
@app.route("/missions", methods=["GET"])
def list_missions():
    try:
        missions = mission_manager.get_all_missions()
        return jsonify(missions), 200

    except Error:
        app.logger.exception("Database error while fetching missions")
        return jsonify({
            "error": "Could not fetch missions"
        }), 500


# Get one mission by ID
@app.route("/missions/<int:mission_id>", methods=["GET"])
def get_mission(mission_id):
    try:
        mission = mission_manager.get_mission_by_id(mission_id)

        if mission is None:
            return jsonify({
                "error": "Mission not found"
            }), 404

        return jsonify(mission), 200

    except Error:
        app.logger.exception("Database error while fetching mission")
        return jsonify({
            "error": "Could not fetch mission"
        }), 500


# Update mission status
@app.route("/missions/<int:mission_id>/status", methods=["PATCH"])
def change_mission_status(mission_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON request body is required"}), 400

    new_status = data.get("status")

    allowed_statuses = [
        "Pending",
        "Assigned",
        "In Progress",
        "Completed",
        "Failed",
        "Cancelled"
    ]

    if new_status not in allowed_statuses:
        return jsonify({
            "error": "Invalid mission status"
        }), 400

    try:
        updated = mission_manager.update_mission_status(
            mission_id, new_status
        )

        if not updated:
            return jsonify({
                "error": "Mission not found"
            }), 404

        return jsonify({
            "message": "Mission status updated successfully"
        }), 200

    except Error:
        app.logger.exception("Database error while updating mission")
        return jsonify({
            "error": "Could not update mission status"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)