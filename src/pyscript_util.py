"""PyScript環境でのみ使える便利機能."""

from js import console


def log(mes: str):
    console.log(mes)
