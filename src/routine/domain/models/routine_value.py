
class RoutineValue():
    """ Classe représentant une valeur de routine journalière. """
    def __init__(self, value: list[float]):
        self.routine_value_id = None
        self.routine_id = None
        self.value = value
        self.recorded_at = None

    # TODO