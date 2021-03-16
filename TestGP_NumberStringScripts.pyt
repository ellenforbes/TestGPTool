import arcpy
import numpy as np
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [sequentialNumbering]

class sequentialNumbering(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Run Sequential Numbering"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter("inputFC","Input Feature Class","Input","GPFeatureLayer","Required")
        param1 = arcpy.Parameter("field","Field For Sequential Numbering","Input", "Field","Required")
        param1.filter.list = ['TEXT']
        param1.parameterDependencies = [param0.name]
        param2 = arcpy.Parameter("startnumber","Starting Number","Input", "Double","Required")
        param3 = arcpy.Parameter("jumpnumber","Interval Number","Input", "Double","Required")
        params = [param0, param1, param2, param3]
        return params

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.env.overwriteOutput = True

        #Define Variables
        inputFC = parameters[0].valueAsText
        field = parameters[1].valueAsText
        startnumber = int(parameters[2].valueAsText)
        jumpnumber = int(parameters[3].valueAsText)

        #Make Calculations
        count = arcpy.GetCount_management(inputFC)
        maxrecords_string = str(count)
        maxrecords = int(maxrecords_string)
        stopnumber = maxrecords*jumpnumber+startnumber+1

        #Define Numbers
        array = np.arange(start=startnumber, stop=stopnumber, step=jumpnumber)
        valuelist = np.ndarray.tolist(array)

        #Iterate and Populate
        i = 0
        with arcpy.da.UpdateCursor(inputFC, (field)) as cursor:
            for row in cursor:
                row[0] = "UID" + str(valuelist[i]).zfill(6)
                cursor.updateRow(row)
                i = i+1

        arcpy.AddMessage("Calculated sequential numbers for " + inputFC)

        return