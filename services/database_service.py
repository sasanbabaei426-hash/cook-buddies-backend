import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

# ----------------------------------------
# CONNECTION
# ----------------------------------------

def get_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))


# ----------------------------------------
# GET USERS (for matching)
# ----------------------------------------

def get_users_from_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               cuisine_preference,
               role_preference,
               availability,
               introversion_level,
               location_zone,
               social_score,
               trust_score
        FROM users;
    """)

    rows = cursor.fetchall()

    users = []

    for row in rows:
        users.append({
            "id": row[0],
            "cuisine_preference": row[1],
            "role_preference": row[2],
            "availability": row[3],
            "introversion_level": row[4],
            "location_zone": row[5],
            "social_score": float(row[6]),
            "trust_score": float(row[7])
        })

    cursor.close()
    conn.close()

    return users


# ----------------------------------------
# SAVE SESSION RESULT
# ----------------------------------------

def save_session_result(data, scores, best_match, match_score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions (
            user_id,
            food_quality,
            comfort_rating,
            awkwardness,
            social_interaction,
            safety_rating,
            attendance,
            experience_score,
            social_score,
            trust_score,
            session_score,
            new_score,
            trust_level,
            best_match,
            match_score
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("user_id"),
        data.get("food_quality"),
        data.get("comfort_rating"),
        data.get("awkwardness"),
        data.get("social_interaction"),
        data.get("safety_rating"),
        data.get("attendance"),
        scores["experience_score"],
        scores["social_score"],
        scores["trust_score"],
        scores["session_score"],
        scores["new_score"],
        scores["trust_level"],
        best_match,
        match_score
    ))

    conn.commit()
    cursor.close()
    conn.close()


# ----------------------------------------
# CREATE NEW USER (registration)
# ----------------------------------------

def create_user(data):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = generate_password_hash(data.get("password"))

    cursor.execute("""
        INSERT INTO users (
            name,
            email,
            password,
            student_id,
            university,
            photo_url,
            cuisine_preference,
            role_preference,
            availability,
            introversion_level,
            location_zone,
            social_score,
            trust_score
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        data.get("name"),
        data.get("email"),
        hashed_password,
        data.get("student_id"),
        data.get("university", "University of Pécs"),
        data.get("photo_url"),
        data.get("cuisine_preference"),
        data.get("role_preference"),
        data.get("availability"),
        data.get("introversion_level"),
        data.get("location_zone"),
        4.0,
        4.0
    ))

    new_user_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return new_user_id
# ----------------------------------------
# GET ALL USERS (for frontend list)
# ----------------------------------------

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               name,
               email,
               student_id,
               university,
               photo_url,
               cuisine_preference,
               role_preference,
               availability,
               introversion_level,
               location_zone,
               social_score,
               trust_score
        FROM users
        ORDER BY id;
    """)

    rows = cursor.fetchall()

    users = []

    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "student_id": row[3],
            "university": row[4],
            "photo_url": row[5],
            "cuisine_preference": row[6],
            "role_preference": row[7],
            "availability": row[8],
            "introversion_level": row[9],
            "location_zone": row[10],
            "social_score": float(row[11]),
            "trust_score": float(row[12])
        })

    cursor.close()
    conn.close()

    return users


# ----------------------------------------
# GET ONE USER BY ID
# ----------------------------------------

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               name,
               email,
               student_id,
               university,
               photo_url,
               cuisine_preference,
               role_preference,
               availability,
               introversion_level,
               location_zone,
               social_score,
               trust_score
        FROM users
        WHERE id = %s;
    """, (user_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "student_id": row[3],
        "university": row[4],
        "photo_url": row[5],
        "cuisine_preference": row[6],
        "role_preference": row[7],
        "availability": row[8],
        "introversion_level": row[9],
        "location_zone": row[10],
        "social_score": float(row[11]),
        "trust_score": float(row[12])
    }


# ----------------------------------------
# SAVE MESSAGE
# ----------------------------------------

def save_message(sender_id, receiver_id, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, message)
        VALUES (%s, %s, %s)
    """, (sender_id, receiver_id, message))

    conn.commit()
    cursor.close()
    conn.close()


# ----------------------------------------
# GET MESSAGES BETWEEN TWO USERS
# ----------------------------------------

def get_messages(user1, user2):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sender_id, receiver_id, message
        FROM messages
        WHERE (sender_id=%s AND receiver_id=%s)
           OR (sender_id=%s AND receiver_id=%s)
        ORDER BY id
    """, (user1, user2, user2, user1))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows