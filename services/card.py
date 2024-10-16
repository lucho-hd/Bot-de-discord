from database.firebase_config import db

def get_all_cards():
    cards_ref = db.collection('cards').stream()
    cards = [card.to_dict() for card in cards_ref]
    return cards

def save_card_to_user(user_id: str, card: dict[str, str]):
    """Guarda las cartas que obtiene el usuario usar el comando '!tirar' en la base de datos"""
    user_ref  = db.collection('user_collections').document(user_id)
    user_data = user_ref.get().to_dict() 

    if not user_data:
        user_data = {'cards': []}
    user_data['cards'].append(card)
    user_ref.set(user_data)


def get_user_collection(user_id: str):
    """Obtiene la coleccion de cartas de un usuario desde la base de datos"""
    user_ref  = db.collection('user_collections').document(user_id)
    user_data = user_ref.get().to_dict() 

    if not user_data or 'cards' not in user_data:
        return []
        
    return user_data['cards']