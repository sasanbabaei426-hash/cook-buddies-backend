from flask import Blueprint, request, jsonify

from services.scoring_service import calculate_scores
from services.matching_service import find_best_match
from services.database_service import (
    save_session_result,
    create_user,
    get_all_users,
    get_user_by_id,
    save_message,
    get_messages
)

calculate_bp = Blueprint("calculate", __name__)


@calculate_bp.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

    user_id = data.get("user_id")
    current_user = get_user_by_id(user_id)

    if current_user is None:
        return jsonify({"error": "User not found"}), 404

    full_data = {
        **data,
        "cuisine_preference": current_user["cuisine_preference"],
        "role_preference": current_user["role_preference"],
        "availability": current_user["availability"],
        "introversion_level": current_user["introversion_level"],
        "location_zone": current_user["location_zone"]
    }

    scores = calculate_scores(full_data)

    best_match, match_score = find_best_match(
        full_data,
        scores["social_score"],
        scores["trust_score"]
    )

    save_session_result(
        full_data,
        scores,
        best_match,
        match_score
    )

    return jsonify({
        "user_id": user_id,
        "current_user": current_user["name"],
        "new_score": scores["new_score"],
        "trust_level": scores["trust_level"],
        "experience_score": scores["experience_score"],
        "social_score": scores["social_score"],
        "trust_score": scores["trust_score"],
        "session_score": scores["session_score"],
        "best_match": best_match,
        "match_score": match_score,
        "saved": True
    })


@calculate_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    new_user_id = create_user(data)

    return jsonify({
        "message": "User registered successfully",
        "user_id": new_user_id
    })


@calculate_bp.route("/users", methods=["GET"])
def users():
    all_users = get_all_users()

    return jsonify(all_users)


@calculate_bp.route("/send_message", methods=["POST"])
def send_message_route():
    data = request.json

    save_message(
        data["sender_id"],
        data["receiver_id"],
        data["message"]
    )

    return jsonify({"status": "sent"})


@calculate_bp.route("/messages/<int:user1>/<int:user2>", methods=["GET"])
def get_chat(user1, user2):
    messages = get_messages(user1, user2)

    result = []

    for msg in messages:
        result.append({
            "sender_id": msg[0],
            "receiver_id": msg[1],
            "message": msg[2]
        })

    return jsonify(result)