from database.firebase_config import db

def save_user_progress(user_id: str, messages_send: int, reactions_made: int, extra_rolls: int):
    """Guarda el progreso del usuario en Firestore."""
    user_ref = db.collection('user_progress').document(user_id)
    user_ref.set({
        'messages_sent': messages_send,
        'reactions_made': reactions_made,
        'extra_rolls': extra_rolls,
    })

def get_user_progress(user_id: str):
    """Obtiene el progreso del usuario desde Firestore."""
    user_ref  = db.collection('user_progress').document(user_id)
    user_data = user_ref.get().to_dict()
    return user_data if user_data else {'message_sent': 0, 'reactions_made': 0, 'extra_rolls': 0} 