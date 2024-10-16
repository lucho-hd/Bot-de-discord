def get_quality_color(quality):
         """Devuelve un color basado en la calidad de la carta"""  
         colors = {
             "Común": 0x808080,
             "Rara": 0x0000FF,
             "Épica": 0x800080,
             "Legendaria": 0xFFD700
         }
         return colors.get(quality, 0xFFFFFF)