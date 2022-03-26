# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations


def remove_none(obj):
    if isinstance(obj, list):
        return [i for i in obj if i is not None]
    elif isinstance(obj, tuple):
        return tuple(i for i in obj if i is not None)
    elif isinstance(obj, set):
        return obj - {None}
    elif isinstance(obj, dict):
        return {k: v for k, v in obj.items() if None not in (k, v)}
