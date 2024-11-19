from classes.XML_DAO import MazeDAOXML
from classes.CSV_DAO import MazeDAOCSV

class FactoryDAO:
    def __init__(self, database, filename):
        self.database = database
        self.filename = filename

    def create_dao(self, file_type):
        filename = f"{self.filename}.{file_type}"
        return MazeDAOXML(self.database, filename) if file_type == 'xml' else MazeDAOCSV(self.database, filename)
