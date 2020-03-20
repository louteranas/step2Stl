#! /usr/bin/env python


import random
import os
import sys
import time
import json
# from pynput import keyboard


from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Extend.DataExchange import read_step_file as readStepFile
from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.Tesselator import ShapeTesselator
from OCC.Extend.DataExchange import write_stl_file



class Parser:
    def __init__(self, display = False, filePath = '/home/ananas/Documents/srcAlma/poc_webgl/stepFiles/', fileName = '33333.stp'):#'02_OUTILLAGE.stp'):
        self.path = filePath
        self.name = fileName
        self.display = display
        self.folder = "model_" + self.name.split('.')[0]
        self.dataStruct = {}

    def printStart(self, outFile):
        print("<x3d width='500px' height='400px'>", file = outFile)
        print("<scene>", file = outFile)


    def printHeader(self, outFile):
        print("<transform translation='0 0 0'>", file = outFile)
        print("<shape>", file = outFile)
        print("<appearance>", file = outFile)
        print("<material diffuseColor='", random.random(), random.random(), random.random(),"'></material>", file = outFile)
        print("</appearance>", file = outFile)

    def printFooter(self, outFile):
        print("</shape>", file = outFile)
        print("</transform>", file = outFile)


    def printEnd(self, outFile):
        print("</scene>", file = outFile)
        print("</x3d>", file = outFile)

    def exportFaces(self, topoDS_Assembly, topoDS_Compound, index):
        folder = self.folder + "/compound" + str(index) + "_faces"
        os.system("mkdir " + folder)
        # outFile = open(folder + "/faces.x3d", "w")
        self.dataStruct["compounds"].append("compound" + str(index) + "_faces")
        # self.printStart(outFile)
        for index, TopAbs_face in enumerate(topoDS_Assembly.faces_from_solids(topoDS_Compound)):
            color = Quantity_Color(random.random(),
                                   random.random(),
                                   random.random(),
                                   Quantity_TOC_RGB)
            tesselator = ShapeTesselator(TopAbs_face)
            tesselator.Compute(True)
            write_stl_file(TopAbs_face, folder + "/faces_"+str(index)+".stl")
        #     ouputString = tesselator.ExportShapeToX3DIndexedFaceSet()
        #     self.printHeader(outFile)
        #     print(ouputString, file = outFile)
        #     self.printFooter(outFile)
        # self.printEnd(outFile)

    def exportCompounds(self, topoDS_Assembly, writeFaces = False):
        self.dataStruct["path"] = self.path + self.folder
        # outFile = open(folder + "/assembly_" + self.name.split('.')[0] +".x3d", "w")
        self.dataStruct["assemblyFile"] = "assembly_" + self.name.split('.')[0] +".x3d"
        self.dataStruct["compounds"] = []
        # self.printStart(outFile)
        for index, topoDS_compound in enumerate(topoDS_Assembly.solids()):
            color = Quantity_Color(random.random(),
                                   random.random(),
                                   random.random(),
                                   Quantity_TOC_RGB)
            tesselator = ShapeTesselator(topoDS_compound)
            tesselator.Compute(True)
            ouputString = tesselator.ExportShapeToX3DIndexedFaceSet()
            write_stl_file(topoDS_compound, self.folder + "/compound_"+str(index)+"_"+ self.name.split('.')[0] +".stl")
            # self.exportObj(coords)
            # normals = ouputString.split("<Normal vector='")[1].split(" '></Normal>")[0].split(" ")
            # normals = [float(item) for item in normals]
            # print(len(normals))
            # self.printHeader(outFile)
            # print(ouputString, file = outFile)
        #     self.printFooter(outFile)
            self.exportFaces(topoDS_Assembly, topoDS_compound, index)
        # self.printEnd(outFile)
    def exportObj(self, coords):
        zfile = open('object.obj', 'w')
        for index in range(0, len(coords), 3):
            print("v", coords[index], coords[index+1], coords[index+2], file = zfile)

        for index in range(0, len(coords)//3, 3):
            print("f", index, index+1, index+2, file = zfile)

    def importStep(self):
        if(self.display) : self.display.EraseAll()
        assembly = readStepFile(self.path+self.name)
        os.system("mkdir " + self.folder)
        write_stl_file(assembly, self.folder + "/assembly_"+ self.name.split('.')[0] +".stl")

        topoDS_Assembly = TopologyExplorer(assembly)

        self.exportCompounds(topoDS_Assembly)

        for compound in topoDS_Assembly.solids():
            color = Quantity_Color(random.random(),
                                   random.random(),
                                   random.random(),
                                   Quantity_TOC_RGB)
            if(self.display) : self.display.DisplayColoredShape(compound, color)
        if(self.display) : self.display.FitAll()
        configFile = open('config.json', "w")
        json.dump(self.dataStruct, configFile)
        print("end")
