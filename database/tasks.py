from database.firebase_config import db
from datetime import datetime, timedelta

def save_user_progress(user_id: str, messages_send: int, reactions_made: int, extra_rolls: int):
    """Guarda el progreso del usuario en Firestore."""
    user_ref = db.collection('user_progress').document(user_id)
    user_ref.set({
        'messages_sent': messages_send,
        'reactions_made': reactions_made,
        'extra_rolls': extra_rolls,
        'last_reset': datetime.now()
    }, merge=True)

def get_user_progress(user_id: str):
    """Obtiene el progreso del usuario desde Firestore."""
    user_ref  = db.collection('user_progress').document(user_id)
    user_data = user_ref.get().to_dict()

    if not user_data:
        return {'messages_sent': 0, 'reactions_made': 0, 'extra_rolls': 0, 'last_reset': datetime.now()}

    last_reset = user_data.get('last_reset')

    if last_reset:
        last_reset = last_reset.replace(tzinfo=None)
        if datetime.now() - last_reset >= timedelta(days=1):
            user_data['messages_sent'] = 0
            user_data['reactions_made'] = 0
            user_data['last_reset'] = datetime.now()

    return user_data
