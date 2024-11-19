from abc import ABC, abstractmethod

class MazeDAO(ABC):
    # creation of main DAO class
    @abstractmethod
    def __init__(self, database, filename):
        self.database = database
        self.filename = filename

    @abstractmethod
    def save_maze(self, input_maze):
        pass

    @abstractmethod
    def load_maze(self, level):
        return np.array([])

    @abstractmethod
    def get_all_levels(self):
        return []
