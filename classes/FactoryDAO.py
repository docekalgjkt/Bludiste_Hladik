from classes.XML_DAO import MazeDAOXML
from classes.CSV_DAO import MazeDAOCSV
from classes.TXT_DAO import MazeDAOText


class FactoryDAO:
    def __init__(self, database, filename):
        self.database = database
        self.filename = filename

    def create_dao(self, file_type):
        filename = f"{self.filename}.{file_type}"
        if file_type == "xml":
            return MazeDAOXML(self.database, filename)
        elif file_type == "csv":
            return MazeDAOCSV(self.database, filename)
        elif file_type == "txt":
            return MazeDAOText(self.database, filename)
