# -*- coding: utf-8 -*-
import arcpy
from arcpy import env
import time
start = time.time()
try:
    # Check out the Network Analyst extension license
    arcpy.CheckOutExtension("Network")
    # Set environment settings
    env.workspace = "G:/SUTPC-DZ/bus/成果/n0527.gdb/s0527"
    env.overwriteOutput = True
    # Set local variables
    inNetworkDataset = "s0527_ND"
    impedanceAttribute = "Length"
    #inAddressLocator = "SanFranciscoLocator"
    #inAddressTable = "C:/data/StopAddresses.csv"
    #inAddressFields = "Street Address VISIBLE NONE"
    #outStops = "GeocodedStops"
    #rootdir = r'G:\diaocha\2'
    #list = os.listdir(rootdir)
    #path = os.path.join(rootdir, list[i])
    #mxd = arcpy.mapping.MapDocument(r"G:/SUTPC-DZ/bus/1.mxd")
    for i  in range(1,1179):
        outNALayerName = str(i)
        outLayerFile = r"G:/SUTPC-DZ/bus/lyr" + "/" + outNALayerName + ".lyr"
        # Create a new Route layer. For this scenario, the default value for all the
        # remaining parameters statisfies the analysis requirements
        outNALayer = arcpy.na.MakeRouteLayer(inNetworkDataset, outNALayerName,
                                            impedanceAttribute)#,UTurn_policy='ALLOW_DEAD_ENDS_AND_INTERSECTIONS_ONLY —U-turns',accumulate_attribute_name='Length',output_path_shape='TRUE_LINES_WITHOUT_MEASURES'
        # Get the layer object from the result object. The route layer can now be
        # referenced using the layer object.
        outNALayer = outNALayer.getOutput(0)
        print outNALayer
        # Get the names of all the sublayers within the route layer.
        subLayerNames = arcpy.na.GetNAClassNames(outNALayer)
        # Stores the layer names that we will use later
        stopsLayerName = subLayerNames["Stops"]
        shpfile1=r'C:/Users/SUTPC/Desktop/wandergis-coordTransform_py-7adb3fe/%d.shp'%i
        arcpy.na.AddLocations(outNALayer, "Stops", shpfile1, "", "")#,snap_to_position_along_network='SNAP',snap_offset=0
        try:
            arcpy.na.Solve(outNALayer,"SKIP","CONTINUE",)# "100 Meters"
        except Exception as e:
            print str(e)
        arcpy.management.SaveToLayerFile(outNALayer, outLayerFile, "RELATIVE")
        lyrFile = arcpy.mapping.Layer(outLayerFile)
        for layer in lyrFile:
            #print layer.name.lower()
            if layer.name.lower() == "routes":
                path = r"G:/SUTPC-DZ/bus/20/%d.shp" %i
                temshp=arcpy.CopyFeatures_management(layer, path)
               # arcpy.mapping.RemoveLayer(arcpy.mapping.ListDataFrames(mxd)[0], temshp)
            #for df in arcpy.mapping.ListDataFrames(mxd)[0]:
                #arcpy.mapping.RemoveLayer(arcpy.mapping.ListDataFrames(mxd)[0],layer)
        del lyrFile
        del outNALayer #卸载窗口
        print '成功生成%d条公交'%i
        end = time.time()
        print end - start
    # Geocode the stop locations from a csv file containing the addresses.
    # The Geocode Addresses tool can use a text or csv file as input table
    # as long as the first line in the file contains the field names.
    #arcpy.geocoding.GeocodeAddresses(inAddressTable, inAddressLocator,
                                   #  inAddressFields, outStops)
    # Load the geocoded address locations as stops mapping the address field from
    # geocoded stop features as Name property using field mappings.
    #fieldMappings = arcpy.na.NAClassFieldMappings(outNALayer, stopsLayerName)
    #fieldMappings["Name"].mappedFieldName = "Address"
    #arcpy.na.AddLocations(outNALayer, stopsLayerName, outStops, fieldMappings,
                   #       "", exclude_restricted_elements="EXCLUDE")
    # Solve the route layer, ignore any invalid locations such as those that
    # can not be geocoded
    #arcpy.na.Solve(outNALayer, "SKIP")
    # Save the solved route layer as a layer file on disk with relative paths
    #arcpy.management.SaveToLayerFile(outNALayer, outLayerFile, "RELATIVE")
    print "Script completed successfully"

except Exception as e:
    # If an error occurred, print line number and error message
    import traceback, sys

    tb = sys.exc_info()[2]
    print "An error occured on line %i" % tb.tb_lineno
    print str(e)
end = time.time()
print end-start
