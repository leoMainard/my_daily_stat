
class Routine():
    """ Classe représentant une routine journalière."""
    def __init__(self, type: str, tags:list[str], description:str):
        self.routine_id = None
        self.user_id = None
        self.type = type
        self.tags = tags
        self.description = description
        self.created_at = None
        self.updated_at = None

    # TODO