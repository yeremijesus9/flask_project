USERS = [
    {"id": 1, "name": "Yeremi", "role": "Admin", "color": "#ffd166"},
    {"id": 2, "name": "German", "role": "Editor", "color": "#7bdff2"},
    {"id": 3, "name": "Yoandres", "role": "Guest", "color": "#b2f7ef"},
]


def get_users():
    return USERS


def get_user_by_id(user_id):
    for user in USERS:
        if user["id"] == user_id:
            return user
    return None


def get_summary():
    return {
        "total_users": len(USERS),
        "roles": [user["role"] for user in USERS],
        "idea": "El servicio guarda los datos y las rutas solo los muestran.",
    }
