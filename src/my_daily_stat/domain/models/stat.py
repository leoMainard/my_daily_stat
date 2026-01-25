
class Stat():
    """ Classe représentant une statistique journalière."""
    def __init__(self, type: str, tags:list[str], description:str):
        self.stat_id = None
        self.user_id = None
        self.type = type
        self.tags = tags
        self.description = description
        self.creation_date = None

    # TODO