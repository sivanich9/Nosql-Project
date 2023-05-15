# importing the required packages
import os
import json
import xml.etree.ElementTree as ET


class XMLParser:
    def __init__(self, xmlFile):
        """
        object takes in the required XML file and creates an XML tree for parsing
        """
        self.xmlFile = xmlFile
        self.tree = ET.parse(self.xmlFile)
        self.root = self.tree.getroot()

        self.processes = []
        self.pigFile = open("pig_script.pig","w+")
        self.dataset = None
        self.typeDef = {}
        self.dumpVariable = "records"
        self.outputFile = "./pig_xml"
        self.defaultName = "records"




    def parseXML(self):
        """
        parse XML method which given an XML file, parses it and gets all the processes
        """

        for item in self.root.findall(".//"):
            # iterate child elements of item

            if item.tag == "inputfile":
                self.dataset = item.text


            elif item.tag == "defaultname":
                self.defaultName = item.text

            elif item.tag == "delimiter":
                self.delimiter = item.text


            elif item.tag == "dumpvar":
                self.dumpVariable = item.text


            elif item.tag == "outputfile":
                self.outputFile = item.text

            elif item.tag == "columns":
                col = None
                for typedef in item:
                    if typedef.tag == "col":
                        col = typedef.text
                    elif typedef.tag == "type":
                        self.typeDef[col] = typedef.text
                        col = None


            # checks for the process tag and iterates over the child elements of process
            elif item.tag == "process":
                for child in item:
                    if child.tag == "name":
                        process = {}
                        process["name"] = child.text
                        self.processes.append(process)

                    elif child.tag == "table":
                        self.processes[-1]["table"] = child.text

                    elif child.tag == "table1":
                        self.processes[-1]["table1"] = child.text

                    elif child.tag == "column":
                        self.processes[-1]["column"] = child.text

                    elif child.tag == "column1":
                        self.processes[-1]["column1"] = child.text

                    elif child.tag == "variable":
                        self.processes[-1]["variable"] = child.text

                    elif child.tag == "task":
                        self.processes[-1]["task"] = child.text

                    elif child.tag == "condition":
                        self.processes[-1]["condition"] = child.text

                    elif child.tag == "clause":
                        self.processes[-1]["clause"] = child.text



    def writeScript(self):
        typeString = ""
        for key, value in self.typeDef.items():
            typeString += "{}:{},".format(key,value)
        typeString = typeString[:-1]

        if self.delimiter == "space":
            loadLine = "records = LOAD '{}' USING PigStorage(' ') AS ({});\n".format(self.dataset, typeString)
            self.pigFile.write(loadLine)


        previousVariable = self.defaultName
        for process in self.processes:
            if process["task"] == "filter":
                scriptline = "{} = FILTER {} by {} {} '{}';\n".format(process["name"], previousVariable, process["column"], process["condition"], process["clause"])
                self.pigFile.write(scriptline)

            elif process["task"] == "group":
                scriptline = "{} = GROUP {} by {};\n".format(process["name"], previousVariable, process["column"])
                self.pigFile.write(scriptline)

            elif process["task"] == "distinct":
                scriptline = "{} = DISTINCT {};\n".format(process["name"], process["table"])
                self.pigFile.write(scriptline)

            elif process["task"] == "cross":
                scriptline = "{} = CROSS {},{};\n".format(process["name"], process["table"], process["table1"])
                self.pigFile.write(scriptline)

            elif process["task"] == "join":
                scriptline = "{} = JOIN {} BY {},{} BY {};\n".format(process["name"], process["table"], process["column"], process["table1"], process["column1"])
                self.pigFile.write(scriptline)

            elif process["task"] == "limit":
                scriptline = "{} =  LIMIT {} {};\n".format(process["name"], process["table"], process["clause"])
                self.pigFile.write(scriptline)

            elif process["task"] == "order":
                scriptline = "{} =  ORDER {} BY {};\n".format(process["name"], process["table"], process["column"])
                self.pigFile.write(scriptline)



        storeLine = "STORE {} INTO '{}';".format(self.dumpVariable, self.outputFile)
        self.pigFile.write(storeLine)
        self.pigFile.close()

        self.executeScript()


    def executeScript(self):
        os.system("pwd")
        os.system("pig pig_script.pig")



if __name__ == "__main__":
    xmlParser = XMLParser("./ingest.xml")
    xmlParser.parseXML()
    print(xmlParser.dataset)
    print(xmlParser.typeDef)
    print(xmlParser.processes)
    xmlParser.writeScript()
