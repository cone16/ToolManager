import re
from sre_constants import RANGE
from config import *
import ToolManager_UI

class ToolManager():

    def __init__(self, tDFile, questionWriteFile):
        self.toolDataFile = tDFile
        self.writeFileYesNo = questionWriteFile
        
        self.HEADER = ['ToolID'], ['ToolNumber'],['ToolName'], ['ToolNoseRadius'], ['isRotary'], ['ToolCounterClockwise'], ['ToolY_Stroke']

        self.groupNumber = []
        self.tID = []
        self.tOffsNumber = []
        self.tName = []
        self.tNoseRadius = []
        self.tIsRotary = []
        self.tCCW = []
        self.tY = []

        self.getToolData()

    # Get Tool Data from File

    def getToolData(self):
        countLinesWithSameBeginning = 0
        countGroupNumbers = 0

        with open(self.toolDataFile, 'r') as file:
            for line in file:
                # first, find all Values and Save them in a List
                # print(line)

                if str(line).find('ShapeData') != -1:
                    if countLinesWithSameBeginning == 1:
                        theSearchedValue = re.findall(r'Value="(.*?)"', line)
                        self.tNoseRadius.append(theSearchedValue)
                        countLinesWithSameBeginning += -29
                    else:
                        countLinesWithSameBeginning += 1
                        continue
                elif str(line).find('GroupNumber') != -1:
                    theSearchedValue = re.findall(r'GroupNumber="(.*?)"', line)
                    self.tOffsNumber.append(theSearchedValue)
                    countGroupNumbers += 1
                    withZeros = str(countGroupNumbers).zfill(4)
                    #print(withZeros)
                    self.groupNumber.append(withZeros)

                if str(line).find('ToolModelId') != -1:
                    theSearchedValue = re.findall(
                        r'ToolModelId="(.*?)"', line)
                    self.tID.append(theSearchedValue)

                if str(line).find(' Name') != -1:
                    theSearchedValue = re.findall(
                        r'" Name="(.*?)"', line)
                    formatedSearchedValue = str(
                        theSearchedValue).replace(",", ".")
                    self.tName.append(formatedSearchedValue)

                if str(line).find('IsMillingTool') != -1:
                    theSearchedValue = re.findall(
                        r'IsMillingTool="(.*?)"', line)
                    self.tIsRotary.append(theSearchedValue)

                if str(line).find('IsCcwDirectionTool') != -1:
                    theSearchedValue = re.findall(
                        r'IsCcwDirectionTool="(.*?)"', line)
                    self.tCCW.append(theSearchedValue)

                if str(line).find('ToolShiftY') != -1:
                    theSearchedValue = re.findall(
                        r'ToolShiftY="(.*?)"', line)
                    self.tY.append(theSearchedValue)

            if self.writeFileYesNo == "Yes":
                return self.writeToFile()
            elif self.writeFileYesNo == "No":
                return self.printToConsole()
            elif self.writeFileYesNo == "Mod":
                return(self.groupNumber, self.tID,  self.tOffsNumber, self.tName, self.tNoseRadius,
                       self.tIsRotary, self.tCCW, self.tY)
            else:
                print("Not a valid option. Programm Aborted")
                return 1

    def printToConsole(self):

        print(str(self.HEADER).strip("()\n"))
        length = len(self.tName)

        for i in range(length):
            print(str(self.groupNumber[i]), ',',
                  str(self.tID[i]), ',',
                  str(self.tOffsNumber[i]), ',',
                  str(self.tName[i]), ',',
                  str(self.tNoseRadius[i]), ',',
                  str(self.tIsRotary[i]), ',',
                  str(self.tCCW[i]), ',',
                  str(self.tY[i]))

        print("converting accomplished.")
        return 0

    def writeToFile(self, finalUISaveFile):

        with open(finalUISaveFile, 'a') as finalFile:
            # get the length of one of the 7 Values to iterate through the list
            length = len(self.tName)
            # build the header of the File for the Excel list
            finalFile.write(str(self.HEADER).strip("()"))
            finalFile.write('\n')
            for i in range(length):
                finalFile.write(str(self.groupNumber[i]))
                finalFile.write(',')
                finalFile.write(str(self.tID[i]))
                finalFile.write(',')
                finalFile.write(str(self.tOffsNumber[i]))
                finalFile.write(',')
                finalFile.write(str(self.tName[i]))
                finalFile.write(',')
                finalFile.write(str(self.tNoseRadius[i]))
                finalFile.write(',')
                finalFile.write(str(self.tIsRotary[i]))
                finalFile.write(',')
                finalFile.write(str(self.tCCW[i]))
                finalFile.write(',')
                finalFile.write(str(self.tY[i]))

                finalFile.write('\n')

        print('closing Files')
        print("converting accomplished.")
        return 0

    def saveToList(self, Group, ID, Name, Offset, ToolNoseRadius):
        # When someone hit the Save Button on the Edit Window,
        # write the new information to the List
        length = len(self.groupNumber)
        print(str(Group))
        for entry in Group:
            print(entry)
        for count in range(length):
            if str(count).zfill(4) == str(Group):
                self.groupNumber[count] = Group
                self.tID[count] = ID
                self.tName[count] = Name
                self.tOffsNumber[count] = Offset
                self.tNoseRadius[count] = ToolNoseRadius
                break
            else:
                continue

if __name__ == "__main__":
    ToolManager("ToolModel.TMD", "No")
    pass
