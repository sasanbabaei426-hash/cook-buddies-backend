def calculate_scores(data):
    old_score = data.get("old_score", 3)

    food_quality = data.get("food_quality", 3)
    comfort_rating = data.get("comfort_rating", 3)
    awkwardness = data.get("awkwardness", 3)
    social_interaction = data.get("social_interaction", 3)
    safety_rating = data.get("safety_rating", 3)
    attendance = data.get("attendance", 1)

    adjusted_awkwardness = 6 - awkwardness

    experience_score = (
        0.5 * food_quality +
        0.5 * comfort_rating
    )

    social_score = (
        0.4 * comfort_rating +
        0.3 * adjusted_awkwardness +
        0.3 * social_interaction
    )

    trust_score = (
        0.5 * safety_rating +
        0.5 * (attendance * 5)
    )

    session_score = (
        0.4 * experience_score +
        0.4 * social_score +
        0.2 * trust_score
    )

    if attendance == 1:
        new_score = 0.7 * old_score + 0.3 * session_score
    else:
        new_score = old_score - 0.3

    new_score = max(1, min(5, new_score))

    if new_score >= 4.5:
        trust_level = "Excellent"
    elif new_score >= 3.5:
        trust_level = "Good"
    elif new_score >= 2.5:
        trust_level = "Moderate"
    else:
        trust_level = "Low"

    return {
        "experience_score": round(experience_score, 2),
        "social_score": round(social_score, 2),
        "trust_score": round(trust_score, 2),
        "session_score": round(session_score, 2),
        "new_score": round(new_score, 2),
        "trust_level": trust_level
    }