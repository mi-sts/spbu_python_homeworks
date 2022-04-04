from threading import Lock


class LockDict:
    def __init__(self, locking_dict: dict):
        self.lock = Lock()
        self.locked_dict = locking_dict

    def __enter__(self):
        self.lock.acquire()
        return self

    def __setitem__(self, key, value):
        if self.lock.locked():
            self.locked_dict[key] = value

    def __getitem__(self, item):
        if self.lock.locked():
            return self.locked_dict[item]
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
