import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg
import PySide2.QtCore as qtc
import os, json, sys, hou, time
from .Converters.MegaHouUSD import MegascanUSD
from .HelpUI import HelpUI
from .InPathsWindow import InPathsWindow
from .AssetGalleryWindow import AssetGalleryWindow

initialOutPath = "C:/Users/beeks/OneDrive/Documents/houdini19.5/MegaUSD/USD EXPORTS/"
megascanDirectory = "C:/Users/beeks/OneDrive/Documents/Megascans Library/Downloaded/3d/"

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # Add a title
        self.setWindowTitle("Megascan to USD")

        # Set grid layout
        self.layout = qtw.QGridLayout()
        self.setLayout(self.layout)

        self.buttonFont = qtg.QFont()
        self.buttonFont.setPointSize(12)

        # Create the asset gallery button
        self.assetGalleryButton = qtw.QPushButton("Choose asset gallery", clicked=lambda: self.assetGalleryWindowOpen())
        self.assetGalleryHelpButton = qtw.QPushButton("Help", clicked=lambda: self.helpOpen("assetGallery"))
        self.assetGalleryButton.setFont(self.buttonFont)
        self.assetGalleryHelpButton.setFont(self.buttonFont)
        
        # Create the in paths button
        self.inPathsButton = qtw.QPushButton("Choose Megascan assets", clicked=lambda: self.inPathsWindowOpen())
        self.inPathsHelpButton = qtw.QPushButton("Help", clicked=lambda: self.helpOpen("inPaths"))
        self.inPathsButton.setFont(self.buttonFont)
        self.inPathsHelpButton.setFont(self.buttonFont)
        self.inPathsWindowCheck = 0
        
        # Create the out path label and button
        self.outPath = initialOutPath
        self.outPathButton = qtw.QPushButton("Set new save destination", clicked=lambda: self.outPathWindowOpen())
        self.outPathHelpButton = qtw.QPushButton("Help", clicked=lambda: self.helpOpen("outPath"))
        self.outPathButton.setFont(self.buttonFont)
        self.outPathHelpButton.setFont(self.buttonFont)

        # Create the export USDs button
        self.exportButton = qtw.QPushButton("Export USDs", clicked=lambda: self.exportUSDs())
        self.exportButton.setFont(self.buttonFont)
        self.exportButton.setEnabled(False)

        # Add the widgets
        self.layout.addWidget(self.assetGalleryButton, 0, 0)
        self.layout.addWidget(self.assetGalleryHelpButton, 0, 1)
        self.layout.addWidget(self.inPathsButton, 1, 0)
        self.layout.addWidget(self.inPathsHelpButton, 1, 1)
        self.layout.addWidget(self.outPathButton, 2, 0)
        self.layout.addWidget(self.outPathHelpButton, 2, 1)
        self.layout.addWidget(self.exportButton, 3, 1)

        # Show the app
        self.show()
     
    def assetGalleryWindowOpen(self):
        self.hide()
        self.assetGalleryUI = AssetGalleryWindow()
        self.assetGalleryUI.sig.connect(self.assetGalleryWindowClose)

    def assetGalleryWindowClose(self):
        self.show()

    def inPathsWindowOpen(self):
        self.hide()
        if self.inPathsWindowCheck:
            self.inPathsUI.show()
        else:
            self.inPathsUI = InPathsWindow(megascanDirectory)
            self.inPathsUI.sig.connect(self.inPathsWindowClose)
            self.inPathsWindowCheck = 1
        
    def inPathsWindowClose(self):
        self.show()
        self.exportButton.setEnabled(True)
        self.inPaths = self.inPathsUI.inPaths

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

    def outPathWindowOpen(self):
        self.hide()
        self.outPath = hou.ui.selectFile(start_directory=self.outPath, title = 'Choose USD export folder', file_type=hou.fileType.Directory)
        self.show()

    def helpOpen(self, index):
        self.hide()
        self.helpUI = HelpUI(index, self.outPath)
        self.helpUI.sig.connect(self.helpClose)

    def helpClose(self):
        self.show()



def startPlugin():
    ex = MainWindow()

#app = qtw.QApplication(sys.argv)
#ex = MainWindow()
#app.exec()