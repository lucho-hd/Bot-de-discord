class Card: 
    """
        Inicializa una carta coleccionable.

        Args:
            name (str): El nombre de la carta.
            image_url (str | None): La URL de la imagen de la carta.
            description (str): La descripción de la carta.
    """
    def __init__(self, name: str, image_url: str | None, description: str) -> None:
        self.name        = name
        self.image_url   = image_url 
        self.description = description