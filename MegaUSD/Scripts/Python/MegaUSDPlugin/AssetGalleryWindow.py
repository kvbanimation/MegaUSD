import hou, json, os
import PySide2.QtWidgets as qtw
import PySide2.QtGui as qtg
import PySide2.QtCore as qtc

def startAssetGallerySelection():
    # Open the Solaris desktop in houdini
    desk = hou.ui.desktop('Solaris')
    desk.setAsCurrent()

    ex = AssetGalleryWindow()

class AssetGalleryWindow(qtw.QWidget):
    sig = qtc.Signal()
        
    def __init__(self):
        super().__init__()
        # Add window title
        self.setWindowTitle("Asset gallery selection")

        # Create font
        self.font = qtg.QFont()
        self.font.setPointSize(12)

        # Create layout
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        # Get list of current asset galleries
        self.galleryDir = os.path.dirname(os.path.realpath(__file__)).removesuffix(r"\Scripts\Python\MegaUSDPlugin") + "/USD EXPORTS/Galleries/"
        self.galleries = next(os.walk(self.galleryDir))[2]
        self.galButtonGroup = qtw.QButtonGroup()
        self.galPaths = []
        self.galBoxes = []
        for gallery in self.galleries:
            if gallery != "TEMPLATE.db":
                self.galPaths.append(self.galleryDir + gallery)            
                galName = gallery.removesuffix(".db")

                galBox = qtw.QCheckBox(galName, clicked=lambda: self.countChecked())
                galBox.setFont(self.font)
                self.layout.addWidget(galBox)
                self.galButtonGroup.addButton(galBox)

                self.galBoxes.append(galBox)

        self.selectButton = qtw.QPushButton("Select", clicked=lambda: self.selectionDone())
        self.layout.addWidget(self.selectButton)
        self.selectButton.setEnabled(False)

        self.newGalText = qtw.QLineEdit()
        self.newGalText.setObjectName("newGalName")
        self.newGalText.setPlaceholderText("Enter new gallery name")
        self.layout.addWidget(self.newGalText)
        self.newGalText.editingFinished.connect(self.textEdited)

        self.newGalButton = qtw.QPushButton("Create new gallery", clicked=lambda: self.createNewGal())
        self.layout.addWidget(self.newGalButton)
        self.newGalButton.setEnabled(False)

        self.show()

    def countChecked(self):
        self.checkCount = 0

        for gallery in self.galBoxes:
            if gallery.isChecked():
                self.checkCount += 1

        if self.checkCount == 0:
            self.selectButton.setEnabled(False)
        else:
            self.selectButton.setEnabled(True)

    def textEdited(self):
        curText = self.newGalText.text()
        if curText != "":
            self.newGalButton.setEnabled(True)
        else:
            self.newGalButton.setEnabled(False)
    
    def selectionDone(self):
        for gallery in self.galBoxes:
            if gallery.isChecked():
                index = self.galBoxes.index(gallery)

                self.assetGalleryPath = self.galPaths[index].replace("\\", "/")

        self.gallerySelected = True

        self.closeWindow()
    
    def createNewGal(self):
        templateDB = os.path.dirname(os.path.realpath(__file__)).removesuffix(r"Scripts\Python\MegaUSDPlugin") + r"USD EXPORTS\Galleries\TEMPLATE.db"
        templateDB = templateDB.replace("\\", "/")
        templateDS = hou.AssetGalleryDataSource(templateDB)
        
        self.assetGalleryPath = templateDB.removesuffix("TEMPLATE.db") + self.newGalText.text() + ".db"
        templateDS.saveAs(self.assetGalleryPath)

        self.closeWindow()

    def closeWindow(self):
        self.assetGalleryDS = hou.AssetGalleryDataSource(self.assetGalleryPath)
        hou.ui.setSharedLayoutDataSource(self.assetGalleryDS)

        self.close()

    def closeEvent(self, event):
        self.sig.emit()
        event.accept()