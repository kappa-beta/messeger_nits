class ContextLockedException(Exception):
    """
    Возникает при обращаении к атрибуту контекстной переменной, когда она заблокирована
    """
    pass


class Context:
    """
    Позволяет обращаться к своим атрибутам, если контекстаная переменная разблокирована
    """
    def __init__(self):
        self.is_locked = False

    def lock(self):
        self.is_locked = True

    def unlock(self):
        self.is_locked = False

    def set(self, key, value):
        """
        Создает атрибуты, либо выдает ошибку при заблокированной переменной
        :param key: имя атрибута
        :param value: значение атрибута
        """
        if self.is_locked:
            raise ContextLockedException
        setattr(self, key, value)
