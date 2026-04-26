from services.database_service import get_users_from_database


def role_match(role_a, role_b):
    if role_a == "Flexible" or role_b == "Flexible":
        return 0.8
    elif (role_a == "Host" and role_b == "Guest") or (role_a == "Guest" and role_b == "Host"):
        return 1.0
    elif role_a == role_b:
        return 0.5
    else:
        return 0.6


def location_match(loc_a, loc_b):
    if loc_a == loc_b:
        return 1.0
    elif loc_a == 5 or loc_b == 5:
        return 0.3
    else:
        return 0.6


def find_best_match(data, social_score, trust_score):
    users = get_users_from_database()

    current_user_id = data.get("user_id")
    cuisine = data.get("cuisine_preference")
    role = data.get("role_preference")
    availability = data.get("availability")
    introversion = data.get("introversion_level")
    location = data.get("location_zone")

    best_match = None
    best_score = -1

    for user in users:

        # Do not match user with themselves
        if user["id"] == current_user_id:
            continue

        if user["availability"] != availability:
            continue

        if user["trust_score"] < 2.5:
            continue

        cuisine_score = 1 if user["cuisine_preference"] == cuisine else 0
        role_score = role_match(role, user["role_preference"])
        personality_score = 1 - abs(introversion - user["introversion_level"]) / 4
        social_score_match = 1 - abs(social_score - user["social_score"]) / 4
        trust_score_match = 1 - abs(trust_score - user["trust_score"]) / 4
        location_score = location_match(location, user["location_zone"])

        match_score = (
            0.20 * cuisine_score +
            0.15 * role_score +
            0.20 * personality_score +
            0.15 * social_score_match +
            0.15 * trust_score_match +
            0.15 * location_score
        )

        if match_score > best_score:
            best_score = match_score
            best_match = user["id"]

    return best_match, round(best_score, 2)