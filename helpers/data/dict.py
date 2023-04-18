from collections import defaultdict


class ListHashableDefault(defaultdict):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def __getitem__(self, __key):
        if isinstance(__key, tuple):
            return {_key: self.get(_key) for _key in __key}
        else: 
            return self.get(__key)

class ListHashableDict(dict):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def __getitem__(self, __key):
        if isinstance(__key, tuple):
            return {_key: self.get(_key) for _key in __key}
        else: 
            return self.get(__key)