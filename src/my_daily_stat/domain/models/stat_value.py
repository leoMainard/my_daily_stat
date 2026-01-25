
class StatValue():
    """ Classe représentant une valeur de statistique journalière. """
    def __init__(self, data: list[float]):
        self.stat_value_id = None
        self.stat_id = None
        self.data = data
        self.update_date = None

    # TODO