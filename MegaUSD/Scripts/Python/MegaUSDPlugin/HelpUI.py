import hou, json, os
import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg
import PySide2.QtCore as qtc

class HelpUI(qtw.QWidget):
    sig = qtc.Signal()
       
    def __init__(self, helpIndex, outPath):
        super().__init__()

        self.setFixedWidth(500)

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.info = qtw.QLabel()
        self.info.setWordWrap(True)

        if helpIndex=="inPaths":
            self.setWindowTitle("Megascan selection help")
            self.info.setText("Opening the choose Megascan asset window will reveal a list of all downloaded Megascan 3D assets. Clicking on an asset will select it for conversion. Multiple assets may be selected.\n\nWindow cannot be opened unless an asset gallery has been selected. Selection is reset each time an asset gallery is selected")
        elif helpIndex=="outPath":
            self.setWindowTitle("Output path selection help")
            self.info.setText("Selecting choose new export path will allow you to set a new folder to export to that will only be used on the current set of asset exports. In order to permanently change the export location, change the initialOutPath string variable in the MegaUSDui.py file to your preferred export folder.\n\nThe current export folder is:\n" + outPath)
        elif helpIndex=="assetGallery":
            self.setWindowTitle("Asset gallery selection help")
            self.info.setText("Opening the choose asset gallery window will reveal a list of all current asset gallery databases in the plug-in folder. Clicking on a gallery will select it. This selection is exclusive, so only one gallery may be selected.\n\nYou may create a new asset gallery by entering a name into the text box and pressing the create new asset gallery button.\n\nAny 3D assets already a part of the selected asset gallery will be removed from the list of 3D assets that can be chosen. This means that if a different asset gallery is chosen after assets to import have been selected, it will clear the asset selection.")
        
        self.closeButton = qtw.QPushButton("Close", clicked=lambda: self.closeHelp())

        self.layout.addWidget(self.info)
        self.layout.addWidget(self.closeButton)

        self.show()

    def closeHelp(self):
        self.close()

    def closeEvent(self, event):
        self.sig.emit()
        event.accept()
