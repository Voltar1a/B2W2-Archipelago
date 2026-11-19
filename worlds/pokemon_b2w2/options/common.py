from __future__ import annotations

from typing import Any, Iterable, Self
from Options import OptionDict, OptionSet, OptionError, Toggle


class ExtendedOptionCounter(OptionDict):
    """
    Dictionary of counter settings with min/max bounds and default backfilling
    """
    valid_keys: list[str] = []
    default: dict[str, int] = {}
    individual_min_max: dict[str, tuple[int, int]] = {}
    fill_defaults: bool = True

    def __init__(self, value: Any):
        if isinstance(value, dict):
            res = dict(self.default) if self.fill_defaults else {}
            for k, v in value.items():
                if k not in self.valid_keys:
                    raise OptionError(f"Unknown key '{k}' for {self.__class__.__name__}")
                if k in self.individual_min_max:
                    min_val, max_val = self.individual_min_max[k]
                    if not (min_val <= v <= max_val):
                        raise OptionError(
                            f"Value {v} for '{k}' is out of range [{min_val}, {max_val}] in {self.__class__.__name__}"
                        )
                res[k] = v
            super().__init__(res)
        elif isinstance(value, int):
            res = dict(self.default)
            res["Maximum"] = value
            super().__init__(res)
        else:
            super().__init__(value or dict(self.default))


class ToggleSet(OptionSet):
    """
    OptionSet that supports boolean shorthand or a list of modifier toggles
    """
    auto_add_if_any: str = "Randomise"

    def __init__(self, value: Any):
        if isinstance(value, bool):
            if value:
                super().__init__({self.auto_add_if_any})
            else:
                super().__init__(set())
        elif isinstance(value, (list, set, tuple)):
            norm_map = {k.casefold(): k for k in getattr(self, "valid_keys", [])}
            s = set()
            for x in value:
                x_str = str(x)
                if x_str.casefold() in norm_map:
                    s.add(norm_map[x_str.casefold()])
                else:
                    s.add(x_str)
            if s and self.auto_add_if_any:
                auto_key = norm_map.get(self.auto_add_if_any.casefold(), self.auto_add_if_any)
                s.add(auto_key)
            super().__init__(s)
        else:
            super().__init__(value)

    @classmethod
    def from_any(cls, data: Any) -> Self:
        if isinstance(data, bool):
            return cls(data)
        if isinstance(data, (list, set, tuple)):
            return cls(data)
        if isinstance(data, str):
            if data.lower() in ("true", "1", "on"):
                return cls(True)
            if data.lower() in ("false", "0", "off"):
                return cls(False)
            return cls({data})
        return super().from_any(data)
