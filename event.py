#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import List


class EventData:
    def __init__(self, name: str, data: object):
        self.name = name
        self.data = data


class Observer(ABC):
    @abstractmethod
    def update(self, event: EventData):
        pass


class Emitter:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, data) -> None:
        for observer in self._observers:
            observer.update(EventData(self.__class__.__name__, data))
