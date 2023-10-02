import hou, os, json

#####################################################################################################################################################################################
class MegascanUSD():
    def __init__(self, outPath=None, gallery=None, inPath=None, objName=None, megaName=None):
        self.outPath = outPath
        self.gallery = gallery
        self.inPath = inPath
        self.objName = objName
        self.megaName = megaName
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setInfo(self, outPath=None, gallery=None, inPath=None, objName=None, megaName=None):
        self.outPath = outPath
        self.gallery = gallery
        self.inPath = inPath
        self.objName = objName
        self.megaName = megaName
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setOutPath(self, outPath=None):
        self.outPath = outPath
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setGallery(self, gallery=None):
        self.gallery = gallery
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setInPath(self, inPath=None):
        self.inPath = inPath
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setMegaName(self, megaName=None):
        if megaName is None and self.inPath is not None:
            self.megaName = []

            megaPathDirs = self.inPath.split("/")
            megaFolder = megaPathDirs[-2]
            megaFolderParts = megaFolder.split("_")

            self.megaName = megaFolderParts[-1]
        else:
            self.megaName = megaName
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def setObjName(self, objName=None):
        if objName is None and self.inPath is not None:
            self.objName = []

            if self.megaName is None:
                megaPathDirs = self.inPath.split("/")
                megaFolder = megaPathDirs[-2]
                megaFolderParts = megaFolder.split("_")

                megaName = megaFolderParts[-1]

                jsonFile = self.inPath + megaName + '.json'
            else:
                jsonFile = self.inPath + self.megaName + '.json'
            
            jsonOpen = open(jsonFile)
            jsonData = json.load(jsonOpen)
            jsonName = jsonData.get('name').lower().replace(' ', '_')
            self.objName = jsonName
        else:
            self.objName = objName
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def import3DAsset(self) -> hou.Node:
        # IMPORT THE MEGASCAN MODEL TO A SOP

        # Ask the user for the asset name
        assetName = self.objName

        # Create a subnet with the given asset name
        geoSubNet = hou.node('/obj').createNode('subnet')
        geoSubNet.setName(assetName)

        # Create a geometry node within the subnet
        assetGeo = geoSubNet.createNode('geo')
        assetGeo.setName('Asset_Geometry')

        # Create a file node with the geo node
        assetGeo1 = assetGeo.createNode('file')

        # Set the file parameter using inPath directory and megaName name
        assetGeo1.parm('file').set(self.inPath + self.megaName + "_LOD0.fbx")

        # Create a transform node under the file to set scale
        assetGeo2 = assetGeo1.createOutputNode('xform')
        assetGeo2.parm('scale').set(0.01)

        # Create an attribute delete to get rid of all reference to fbx
        assetGeo3 = assetGeo2.createOutputNode('attribdelete')
        assetGeo3.parm('ptdel').set('fbx_*')

        # Create a null and set its name
        assetGeoNull = assetGeo3.createOutputNode('null')
        assetGeoNull.setName(assetName + '_lod0')

        # Set the display and render flags
        assetGeoNull.setDisplayFlag(True)
        assetGeoNull.setRenderFlag(True)

        # Layout asset geometry node
        assetGeo.layoutChildren(items=(), horizontal_spacing=-1.0, vertical_spacing=-1.0)

        return assetGeo
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def create3DAssetUSD(self): # This will have pretty much the entire code inside it
        # IMPORT THE MEGASCAN MODEL TO A SOP

        # Ask the user for the asset name
        assetName = self.objName

        # Create a subnet with the given asset name
        geoSubNet = hou.node('/obj').createNode('subnet')
        geoSubNet.setName(assetName)

        # Create a geometry node within the subnet
        assetGeo = geoSubNet.createNode('geo')
        assetGeo.setName('Asset_Geometry')

        # Create a file node with the geo node
        assetGeo1 = assetGeo.createNode('file')

        # Set the file parameter using inPath directory and megaName name
        assetGeo1.parm('file').set(self.inPath + self.megaName + "_LOD0.fbx")

        # Create a transform node under the file to set scale
        assetGeo2 = assetGeo1.createOutputNode('xform')
        assetGeo2.parm('scale').set(0.01)

        # Create an attribute delete to get rid of all reference to fbx
        assetGeo3 = assetGeo2.createOutputNode('attribdelete')
        assetGeo3.parm('ptdel').set('fbx_*')

        # Create a null and set its name
        assetGeoNull = assetGeo3.createOutputNode('null')
        assetGeoNull.setName(assetName + '_lod0')

        # Set the display and render flags
        assetGeoNull.setDisplayFlag(True)
        assetGeoNull.setRenderFlag(True)

        # Layout asset geometry node
        assetGeo.layoutChildren(items=(), horizontal_spacing=-1.0, vertical_spacing=-1.0)
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------



        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # CREATE COMPONENT BUILDER

        # Create the subnet node that the component builder will reside in
        stageSubNet = hou.node('/stage').createNode('subnet')

        # Get list of subnet parameters and turn it into a template group
        subNetParmTemplate = stageSubNet.parmTemplateGroup()

        # Define the new parameters (string, operator path, file directory)
        subNetString = hou.StringParmTemplate('name', 'Name', 1)
        subNetOpPath = hou.StringParmTemplate('object', 'SOP Object', 1, string_type=hou.stringParmType.NodeReference)
        subNetFileDir = hou.StringParmTemplate('path', 'Path', 1, string_type=hou.stringParmType.FileReference)

        # Append new parameters to the template list
        subNetParmTemplate.append(subNetString)
        subNetParmTemplate.append(subNetOpPath)
        subNetParmTemplate.append(subNetFileDir)

        # Set parameter changes to subnet
        stageSubNet.setParmTemplateGroup(subNetParmTemplate)

        # Set the subnet node color to blue
        blue = hou.Color((0.094, 0.369, 0.69))
        stageSubNet.setColor(blue)

        # Set the values of the custom parameters
        stageSubNet.parm('name').set(self.objName)
        stageSubNet.parm('object').set(assetGeo.path())
        stageSubNet.parm('path').set(self.outPath)

        # Create the component geometry node used by the component builder
        compGeo = stageSubNet.createNode('componentgeometry')

        # Create the material library node used by the component builder and set its path prefix
        matLib = stageSubNet.createNode('materiallibrary')
        matLib.parm('matpathprefix').set("/ASSET/mtl/")

        # Create the component material node used by the component builder
        compMat = stageSubNet.createNode('componentmaterial')

        # Create the component output node used by the component builder
        compOut = stageSubNet.createNode('componentoutput')

        # Delete the subnet output node
        hou.node('/stage/' + stageSubNet.name() + '/output0').destroy()

        # Create the proper component builder hierarchy
        compOut.setInput(0, compMat)
        compMat.setInput(0, compGeo)
        compMat.setInput(1, matLib)

        # Set the display and render flags
        compOut.setDisplayFlag(True)

        # Organize the subnet nodes
        stageSubNet.layoutChildren(items=(), horizontal_spacing=-1.0, vertical_spacing=-1.0)
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # IMPORT SOP INTO LOP

        # Create the object merge null node as input to the default output in the component geometry node
        objMergeNull = hou.node('/stage/' + stageSubNet.name() + '/' + compGeo.name() + '/sopnet/geo/default').createInputNode(0, 'null')
        objMergeNull.setName('INPUT')

        # Create the object merge node as the input to the null
        objMerge = objMergeNull.createInputNode(0, 'object_merge')

        # Set the object merge path to the custom object parameter on the stage subnet
        objMerge.parm('objpath1').set('`chsop("../../../../object")`')

        # Create a poly reduce node under the null
        polyReduce = objMergeNull.createOutputNode('polyreduce::2.0')

        # Set reduction value
        polyReduce.parm('percentage').set(10)

        # Connect the other output nodes
        hou.node('/stage/' + stageSubNet.name() + '/' + compGeo.name() + '/sopnet/geo/proxy').setInput(0,polyReduce)
        hou.node('/stage/' + stageSubNet.name() + '/' + compGeo.name() + '/sopnet/geo/simproxy').setInput(0,polyReduce)
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------



        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # CREATE MTLX

        # Create the MtlX subnet node in the component builder material library
        self.mtlxSubNet = matLib.createNode('subnet')
        self.mtlxSubNet.setName(self.objName + '_mtlx')

        # Create the surface output node, rename it, and set its color to salmon
        surfOut = self.mtlxSubNet.createNode('subnetconnector')
        surfOut.setName('surface_output')
        salmon = hou.Color((0.996, 0.682, 0.682))
        surfOut.setColor(salmon)

        # Set surface output parameters
        surfOut.parm('connectorkind').set('output')
        surfOut.parm('parmname').set('surface')
        surfOut.parm('parmlabel').set('Surface')
        surfOut.parm('parmtype').set('surface')

        # Create the displacement output node, rename it, and set its color to lavender
        dispOut = self.mtlxSubNet.createNode('subnetconnector')
        dispOut.setName('displacement_output')
        lavender = hou.Color((0.565, 0.494, 0.863))
        dispOut.setColor(lavender)

        # Set displacement outpu parameters
        dispOut.parm('connectorkind').set('output')
        dispOut.parm('parmname').set('displacement')
        dispOut.parm('parmlabel').set('Displacement')
        dispOut.parm('parmtype').set('displacement')

        # Create the materialX surface shader node
        mtlxStdSurf = self.mtlxSubNet.createNode('mtlxstandard_surface')

        # Create a tuple of each texture that needs importing
        texNames = ('Albedo', 'Roughness', 'Normal', 'Displacement')
    
        # Create each imported image node
        albedoImg = self.createMtlxImage(texNames[0])
        roughnessImg = self.createMtlxImage(texNames[1])
        normalImg = self.createMtlxImage(texNames[2])
        displacementImg = self.createMtlxImage(texNames[3])

        # CONNECT TEXTURE PATHS------------------------------------------------------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # CONNECT THE ALBEDO IMAGE NODE

        # Connect the albedo image node to the standard surface
        mtlxStdSurf.setInput(1, albedoImg)

        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # CONNECT THE ROUGHNESS IMAGE NODE

        # Create a vector3 to 3float
        mtlxSep3c = self.mtlxSubNet.createNode('mtlxseparate3c')

        # Connect the nodes
        mtlxStdSurf.setInput(6, mtlxSep3c)
        mtlxSep3c.setInput(0, roughnessImg)

        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # CONNECT THE NORMAL IMAGE NODE

        # Create a mtlx normal map node
        mtlxNormMap = self.mtlxSubNet.createNode('mtlxnormalmap')

        # Connect the nodes
        mtlxStdSurf.setInput(40, mtlxNormMap)
        mtlxNormMap.setInput(0, normalImg)

        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # CONNECT THE DISPLACEMENT IMAGE NODE

        # Create a vector3 to 3float, mtlx remap, mtlx displacement
        mtlxSep3c2 = self.mtlxSubNet.createNode('mtlxseparate3c')
        mtlxRemap = self.mtlxSubNet.createNode('mtlxremap')
        mtlxDisp = self.mtlxSubNet.createNode('mtlxdisplacement')

        # Set the remap out values to between -0.5 and 0.5
        mtlxRemap.parm('outlow').set(-0.5)
        mtlxRemap.parm('outhigh').set(0.5)

        # Set the displacement scale value to 0.01
        mtlxDisp.parm('scale').set(0.001)

        # Connect the nodes
        mtlxDisp.setInput(0, mtlxRemap)
        mtlxRemap.setInput(0, mtlxSep3c2)
        mtlxSep3c2.setInput(0, displacementImg)

        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # MAKE FINAL CONNECTIONS
        surfOut.setInput(0, mtlxStdSurf)
        dispOut.setInput(0, mtlxDisp)

        # Set the render flag
        self.mtlxSubNet.setMaterialFlag(True)

        # Layout the nodes in the mtlx subnet
        self.mtlxSubNet.layoutChildren(items=(), horizontal_spacing=-1.0, vertical_spacing=-1.0)
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------



        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # EXPORT THE USD

        # Set LOP component name
        compOut.parm('rootprim').set('`chs("../name")`')

        # Set USD output location
        compOut.parm('lopoutput').set('`chs("../path")``chs("../name")`/`chs("filename")`')

        # Set up the thumbnail settings
        compOut.parm('thumbnailmode').set(2)

        # Find the imported object bounding box
        #objGeo = assetGeoNull.geometry()
        #objBbox = objGeo.boundingBox()

        # Frame the found bounding box
        #geoPane = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
        #geoViewport = geoPane.curViewport()
        #geoViewport.home()
        #geoViewport.frameBoundingBox(objBbox)

        # Export the USD, generate a thumbnail, and add to the asset gallery
        compOut.parm('execute').pressButton()
        compOut.parm('executerender').pressButton()
        compOut.parm('addtogallery').pressButton()
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def testGalleryUSD():
        #hou.hipFile.clear()

        layout = hou.node('/stage').createNode('layout')
        layout.setName('ASSET_TEST_LAYOUT')

        stage = hou.node('/stage')
        stage.layoutChildren(items=(), horizontal_spacing=-1.0, vertical_spacing=-1.0)
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def listUSDExports(self) -> list: # This is to check for already exported USDs
        if self.outPath is not None:
            exportDirs = next(os.walk(self.outPath))[1]
        else:
            exportDirs = ['No output path set. Use MegascanUSD.setOutPath(self, outPath=None)']

        return exportDirs
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def createMtlxImage(self, texName):
        nodeLoc=self.mtlxSubNet
        fileDir=self.inPath
        megaName=self.megaName

        # Create the mtlx image node to import file to
        mtlxImage = nodeLoc.createNode('mtlximage')
        mtlxImage.setName(texName)
        
        # Use an if statement (with an elif) to single out differences with normal and displacement file names
        # Then set file name
        if (texName == 'Normal'):
            mtlxImage.parm('file').set(fileDir + megaName + '_4K_' + texName + '_LOD0.jpg')
        elif (texName == 'Displacement'):
            mtlxImage.parm('file').set(fileDir + megaName + '_4K_' + texName + '.exr')
        else:
            mtlxImage.parm('file').set(fileDir + megaName + '_4K_' + texName + '.jpg')
        
        # Return the mtlx image node
        return mtlxImage
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
               
#####################################################################################################################################################################################
