class SessionNotFound(Exception):
    def __init__(self, _id: str):
        self._id = _id
        super().__init__(f"Сессия с id {_id} не найдена")
