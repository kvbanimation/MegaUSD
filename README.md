# Megascan to USD
This Houdini plug-in takes in Megascan 3D assets and converts them inside Houdini into USD components and adds them to a specified layout asset gallery.

## Installation
Here are the steps to installing the plug-in to Houdini:
1. Download the zip folder and extract its contents
2. Find the MegaUSD folder and copy it into your Houdini version folder, which should be found in the documents folder
3. Find the MegaUSDPlugin.json file and copty it into the packages folder in the Houdini version folder
4. Those are all of the files that are needed from the zip folder contents

The next step is to set a few paths:
1. Open the megaUSDui.py file found in MegaUSD\Scripts\Python\MegaUSDPlugin\MegaUSDui.py
2. Set the initialOutPath string variable to the path to the plug-in USD EXPORTS folder
3. Set the megascanDirectory string variable to the path to the Megascan Library folder, which should be found in the documents folder
4. Make sure the strings are raw string (r"folder\folder"), using double backslashes ("folder\\folder"), or using forwardslashes ("folder/folder")
5. Open the json file you copied to the packages folder
6. Set the path to the path to the plug-in folder

Not required, but recommended installation steps:
* Adding the layout asset gallery pane tab to the Solaris desktop
    1. Run the Houdini version the plug-in was installed to
    2. Open the Solaris desktop
    3. Open the layout asset gallery pane tab, which is done by pressing the + next to the tabs in the desired pane and selecting: New Pane Tab Type > Solaris > Layout Asset Gallery
    4. Save the Solaris desktop

## How to use
With the plug-in properly installed, upon opening Houdini, a new menu options called "MegaUSD" will appear on the top menu bar. Clicking
it will reveal a menu with two options:
* Megascan USD Converter
* Select Asset Gallery

### Megascan USD Converter
This is used to quickly convert Megascan 3D assets into USD components using the component builder LOP and add them to a layout asset gallery for easy use with the layout LOP

Clicking on the Megascan USD Converter will automatically open the Solaris Desktop, and if the recommended installation step was taken, the layout asset gallery pane tab. It will also open a window with the following options:
* Choose asset gallery
* Choose Megascan assets
* Set new save destination
* Export USDs

#### Choose asset gallery
Opening the choose asset gallery window will reveal a list of all current asset gallery databases in the plug-in folder. Clicking on a gallery will select it. This selection is exclusive, so only one gallery may be selected.

You may create a new asset gallery by entering a name into the text box and pressing the create new asset gallery button.

Any 3D assets already a part of the selected asset gallery will be removed from the list of 3D assets that can be chosen. This means that if a different asset gallery is chosen after assets to import have been selected, it will clear the asset selection.

#### Choose Megascan assets
Opening the choose Megascan asset window will reveal a list of all downloaded Megascan 3D assets. Clicking on an asset will select it for conversion. Multiple assets may be selected.

Window cannot be opened unless an asset gallery has been selected. Selection is reset each time an asset gallery is selected.

#### Set new save destination
Selecting choose new export path will allow you to set a new folder to export to that will only be used on the current set of asset exports. In order to permanently change the export location, change the initialOutPath string variable in the MegaUSDui.py file to your preferred export folder.

It is recommended to not set a one time export folder. This ensures that all assets can be found in one place.

#### Export USDs
Clicking this button will run the converter for each asset selected in the choose Megascan assets window and add them to the layout asset gallery selected in the choose asset gallery window.

This button is disabled until at least one asset has been selected. Since selecting an asset gallery resets asset selection, this button is disabled each time an asset gallery is selected.

### Select Asset Gallery
Opening the choose asset gallery window will automatically open the Solaris Desktop, and if the recommended installation step was taken, the layout asset gallery pane tab. It will also reveal a list of all current asset gallery databases in the plug-in folder. Clicking on a gallery will select it. This selection is exclusive, so only one gallery may be selected.

You may create a new asset gallery by entering a name into the text box and pressing the create new asset gallery button.

This menu selection is used to switch between plug-in layout asset galleries quickly when not also adding any assets to the gallery.

## Known Limitations
This plug-in is currently limited to being used with single asset 3D assets from Megascans. This means that it does not yet function with 3D plant assets, assets with variants, assets that share a name, or non-3D Megascan assets. The keyword here is yet, see below section on future update plans.

Note: Currently, if even just two assets that share a name are selected it will cause an error that stops the converter.

If there are enough downloaded 3D assets from Megascans, the choose Megascan assets window does not currently have a scroll feature. Once again, see below section on future update plans.

## Future Update Plans
Though the plug-in is completely functional for 3D Megascan assets, I am continuing the plug-ins development to address the above limitations and improve features that are already present. Here is a list of updates that I am working on:
* First and foremost, I need to go through and add comments to my code. Parts have comments, but there is still a lot that doesn't. As comments are added I will also be cleaning up the code to make it more efficient.
* Create converter for Megascan assets with variants, including 3D plants
* Create converter for Megascan surfaces, essentially turn them into a USD materialX that will not be added to the layout asset gallery
* Find assets that share a name and have them import as variants
* Create a scroll bar on the asset gallery selection and asset selection windows if the number of items being listed exceeds a certain value
* Change the height map displacement scale based on the size of the asset. This is going to require a decent amount of data to find an optimal mathematically relationship between asset size and displacement scale.
* Setup an installer to reduce the complexity of the plug-in installation process