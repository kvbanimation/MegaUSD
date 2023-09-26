import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg
import PySide2.QtCore as qtc
import os, json, sys, hou, time
from .Utilities.MegaHouUSD import MegascanUSD

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # Add a title
        self.setWindowTitle("Megascan to USD Settings")

        # Set grid layout
        self.layout = qtw.QGridLayout()
        self.setLayout(self.layout)

        self.buttonFont = qtg.QFont()
        self.labelFont = qtg.QFont()
        self.buttonFont.setPointSize(12)
        self.labelFont.setPointSize(10)
        
        # Create the in paths button
        self.inPathsButton = qtw.QPushButton("Choose Megascan assets", clicked=lambda: self.inPathsWindowOpen())
        self.inPathsButton.setFont(self.buttonFont)
        self.inPathsWindowCheck = 0
        
        # Create the out path label and button
        self.outPath = 'C:/Users/beeks/OneDrive/Documents/houdini19.5/MegaUSD/USD EXPORTS/'
        self.outPathLabel = qtw.QLabel('Current save destination:\n' + r'C:\Users\beeks\OneDrive\Documents\houdini19.5\MegaUSD\USD EXPORTS')
        self.outPathLabel.setFont(self.labelFont)
        self.outPathLabel.setAlignment(qtc.Qt.AlignCenter)
        self.outPathButton = qtw.QPushButton("Set new save destination")
        self.outPathButton.setFont(self.buttonFont)

        # Create the export USDs button
        self.exportButton = qtw.QPushButton("Export USDs", clicked=lambda: self.exportUSDs())
        self.exportButton.setFont(self.buttonFont)
        self.exportButton.setEnabled(False)

        # Add the widgets
        self.layout.addWidget(self.inPathsButton, 0, 0)
        self.layout.addWidget(self.outPathLabel, 1, 0)
        self.layout.addWidget(self.outPathButton, 2, 0)
        self.layout.addWidget(self.exportButton, 3, 0)

        # Show the app
        self.show()
    
    def inPathsWindowOpen(self):
        self.hide()
        if self.inPathsWindowCheck:
            self.ui.show()
        else:
            self.ui = InPathsWindow()
            self.ui.sig.connect(self.inPathsWindowClose)
            self.inPathsWindowCheck = 1
        
    
    def inPathsWindowClose(self):
        self.show()
        self.exportButton.setEnabled(True)
        self.inPaths = self.ui.inPaths

    def exportUSDs(self):
        self.curImport = 1
        self.numImports = len(self.inPaths)
        
        self.importStatus = qtw.QStatusBar()
        self.importStatus.setFont(self.labelFont)
        self.layout.addWidget(self.importStatus)
        self.importStatus.showMessage("Working on asset " + str(self.curImport) + "/" + str(self.numImports))
        
        megaHou = MegascanUSD()
        megaHou.setOutPath(self.outPath)

        for path in self.inPaths:
            self.importStatus.showMessage("Working on asset " + str(self.curImport) + "/" + str(self.numImports))
            self.repaint()
            time.sleep(1)

            megaHou.setInPath(path)
            megaHou.setMegaName()
            megaHou.setObjName()

            megaHou.create3DAssetUSD()
            
            self.curImport += 1

        MegascanUSD.testGalleryUSD()

        self.close()
        
        

class InPathsWindow(qtw.QWidget):
    sig = qtc.Signal()
    
    def __init__(self):
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
        self.megaFolderPath = "C:/Users/beeks/OneDrive/Documents/Megascans Library/Downloaded/3d/"
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
    


def startPlugin():
    ex = MainWindow()

#app = qtw.QApplication(sys.argv)
#ex = MainWindow()
#app.exec()