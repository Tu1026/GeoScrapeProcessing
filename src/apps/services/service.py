from abc import ABC, abstractclassmethod


class Service(ABC):
    def __init__(self):
        pass

    @abstractclassmethod
    def returnServiceResults(self):
        pass
