import hou, json, os
import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg
import PySide2.QtCore as qtc

class InPathsWindow(qtw.QWidget):
    sig = qtc.Signal()
    
    def __init__(self, megaDir):
        super().__init__()
        # Add window title
        self.setWindowTitle("Megascan asset selection")

        # Create font
        self.font = qtg.QFont()
        self.font.setPointSize(12)

        # Create layout
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        # Get list of names
        self.megaFolderPath = megaDir
        self.megaFolders = next(os.walk(self.megaFolderPath))[1]
        self.names = []
        self.inPathsList = []
        for folder in self.megaFolders:
            megaPath = self.megaFolderPath + folder + "/"
            self.inPathsList.append(megaPath)

            megaPathDirs = megaPath.split("/")
            megaFolder = megaPathDirs[-2]
            megaFolderParts = megaFolder.split("_")

            megaName = megaFolderParts[-1]

            jsonFile = megaPath + megaName + '.json'

            jsonOpen = open(jsonFile)
            jsonData = json.load(jsonOpen)
            jsonName = jsonData.get('name')#.lower().replace(' ', '_')
            self.names.append(jsonName)

        self.assetBoxes = []

        # Create a check box button for each asset
        for asset in self.names:
            assetBox = qtw.QCheckBox(asset, clicked=lambda: self.countChecked())
            assetBox.setFont(self.font)
            self.layout.addWidget(assetBox)

            self.assetBoxes.append(assetBox)

        self.checkCounter = qtw.QLabel("Assets checked: 0")
        self.layout.addWidget(self.checkCounter)

        self.doneButton = qtw.QPushButton("Done", clicked=lambda: self.selectionDone())
        self.layout.addWidget(self.doneButton)
        self.doneButton.setEnabled(False)

        self.show()

    def countChecked(self):
        self.checkCount = 0

        for asset in self.assetBoxes:
            if asset.isChecked():
                self.checkCount += 1

        self.checkCounter.setText("Assets checked: " + str(self.checkCount))

        if self.checkCount == 0:
            self.doneButton.setEnabled(False)
        else:
            self.doneButton.setEnabled(True)
    
    def selectionDone(self):
        self.inPaths = []
        for asset in self.assetBoxes:
            if asset.isChecked():
                index = self.assetBoxes.index(asset)

                self.inPaths.append(self.inPathsList[index])
        
        self.hide()
        self.sig.emit()