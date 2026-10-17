import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

def loadUI(uiFilename, parent = None):
    path = os.path.join(os.path.dirname(__file__), uiFilename)
    loader = QUiLoader()

    file = QFile(path)

    if not file.exists():
        return None
    
    file.open(QFile.ReadOnly)
    ui = loader.load(file, parent)
    file.close()

    return ui