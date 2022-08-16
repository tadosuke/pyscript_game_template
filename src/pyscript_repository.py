"""PyScript用リポジトリ."""

from model import AbstractRepository
import typing as tp

from js import (
    console,
    localStorage,
)


class PyScriptRepository(AbstractRepository):

    def __init__(self):
        pass

    def save(self, key: str, value: tp.Any):
        localStorage.setItem(key, value)
        console.log(f'save {key}={value}')

    def load(self, key: str, default: tp.Any = None) -> tp.Any:
        value = localStorage.getItem(key)
        console.log(f'load {key}={value}')
        if value is None:
            if default is not None:
                return default
            raise IOError(f'failed to load(key={key})')
        return value
