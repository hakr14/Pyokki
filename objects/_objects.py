from typing import Union

class PType:
    def __init__(self, name: str, colors: tuple[tuple[int, int, int, int], tuple[int, int, int, int], tuple[int, int, int, int]]):
        self.name = name
        self.color, self.light, self.dark = colors
        self.eff: dict["PType", float] = {}

    def effectiveness(self, ptype: "PType", second_type: Union["PType", None] = None):
        if second_type is None:
            return self.eff[ptype]
        else:
            return self.effectiveness(ptype) * self.effectiveness(second_type)

    def __str__(self):
        return self.name