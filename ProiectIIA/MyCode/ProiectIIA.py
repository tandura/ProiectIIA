import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

if sys.version_info < (3, 0):
    raise "must use python 3.4 or greater"

from utils import *
from logic import *

simptomsTag = "Pacientul prezinta simptomele:"
riscTags = "Pacientul prezinta urmatorii factori de risc:"
testTag = "Teste:"
diagnosticTag = "Diagnostic:"

SimptomsValues = {
                    "poliuria": 15, # cele mai comune
                    "polidipsia": 15,
                    "polifagia": 15,
                    "scadere in greutate": 15,
                    "situatii repetate de vedere incetosata":  8, # mai putin comune
                    "mancarime":  8,
                    "deteriorarea vaselor sangvine":  8,
                    "infectii vaginale recurente":  8,
                    "stare accentuata de oboseala":  8
                 }

RiscValues = {
                "Dieta bogata in zahar": 20,
                "Stilul de viata sedentar": 20,
                "Greutate mica la nastere": 20,
                "Varsta": 20,
                "Antecedentele din familie": 20
             }

AcceptedTests = ["FPG", "A1C", "OGTT", "RPG"]
AcceptedDiagnostics = ["Prediabetes", "Diabet", "Nu are diabet"]
IrelevantTests = []
IrelevantSimptoms = []
IrelevantRiscs = []

IrelevantDiagnostic = False
noTestsDone = True

A1C = {}
A1C["Normal"] = Symbol("A1C_Normal")
A1C["Prediabetes"] = Symbol("A1C_Prediabetes")
A1C["Diabetes"] = Symbol("A1C_Diabetes")

FPG = {}
FPG["Normal"] = Symbol("FPG_Normal")
FPG["Prediabetes"] = Symbol("FPG_Prediabetes")
FPG["Diabetes"] = Symbol("FPG_Diabetes")

OGTT = {}
OGTT["Normal"] = Symbol("OGTT_Normal")
OGTT["Prediabetes"] = Symbol("OGTT_Prediabetes")
OGTT["Diabetes"] = Symbol("OGTT_Diabetes")

RPG = {}
RPG["Diabetes"] = Symbol("RPG_Diabetes")

Diabetes = Symbol("Diabetes")
Prediabetes = Symbol("Prediabetes")

def readDefaultInputFile():
    with open(r".\MyCode\DefaultInput.txt") as f:
        #print("File content:")
        #content = ""
        content = f.read()
        
        #check for "IGNORE" tag
        position = content.find("#IGNORE#", 0)
        if position != -1:
            content = content[0:position]
        #print(content + "\n\n")
        
        return content

def splitList(List):
    List = List.replace(".", ",")
    List = List.replace(";", ",")
    List = List.split(",")
    Results = []
    for elem in List:
        if elem.strip() != "":        
            Results.append(elem.strip())

    return Results
    

def parseContent(content):
    global noTestsDone, IrelevantTests

    positionSimptom = content.find(simptomsTag, 0) #get tag positions
    positionRisc = content.find(riscTags, positionSimptom)
    positionTests = content.find(testTag, positionRisc)
    positionDiagnostic = content.find(diagnosticTag, positionTests)

    simptomsList = content[positionSimptom + len(simptomsTag):positionRisc]
    simptomsList = splitList(simptomsList)
    #print("Simptoms:")
    #for simptom in simptomsList:        
    #    print("\t" + simptom)

    riscsList = content[positionRisc + len(riscTags) : positionTests]
    riscsList = splitList(riscsList)
    #print("Riscs:")
    #for risc in riscsList:        
    #    print("\t" + risc)

    testList = content[positionTests + len(testTag) : positionDiagnostic]
    testList = testList.replace(";", ",")
    testList = testList.split(",")
    Results = []
    for elem in testList:
        if elem.strip() != "":        
            Results.append(elem.strip())
    testList = Results
    #print("Tests:")
    #for test in testList:        
    #    print("\t" + test)

    testDict = {}
    if testList[0].strip('.') != "NONE":
        for test in testList:
            test = test.split(" ")
            if test[0] in AcceptedTests:
                testDict[test[0]] = float(test[1])
            else:
                IrelevantTests.append(test[0])
        
        if len(testDict.keys()) > 0:
            noTestsDone = False
    
    diagnostic = content[positionDiagnostic + len(diagnosticTag) : ].strip()
    diagnostic = diagnostic.replace(".", "")
    #print("Diagnostic:\n\t" + diagnostic)

    return (simptomsList, riscsList, testDict, diagnostic)

def InitKB():
    kb = PropKB()

    kb.tell(A1C["Diabetes"] | FPG["Diabetes"] | OGTT["Diabetes"] | RPG["Diabetes"] | '==>' | Diabetes)
    kb.tell(A1C["Prediabetes"] | FPG["Prediabetes"] | OGTT["Prediabetes"] | '==>' | Prediabetes)

    return kb

def processData(simptomsList, riscsList, testDict, diagnostic, kb):
    global IrelevantSimptoms, IrelevantRiscs
    
    Score = 0
    
    for simptom in simptomsList:
        if simptom not in SimptomsValues.keys():
            IrelevantSimptoms.append(simptom)
        else:
            Score += SimptomsValues[simptom]

    for risc in riscsList:
        if risc not in RiscValues.keys():
            IrelevantRiscs.append(risc)
        else:
            Score += RiscValues[risc]

    if "FPG" in testDict.keys():
        if testDict["FPG"] < 5.6: 
            kb.tell(FPG["Normal"])
        else:
            if testDict["FPG"] >= 5.6 and  testDict["FPG"] <= 6.4:
                kb.tell(FPG["Prediabetes"])
            else:
                kb.tell(FPG["Diabetes"])

    if "A1C" in testDict.keys():
        if testDict["A1C"] < 99: 
            kb.tell(A1C["Normal"])
        else:
            if testDict["A1C"] >= 100 and  testDict["A1C"] <= 125:
                kb.tell(A1C["Prediabetes"])
            else:
                kb.tell(A1C["Diabetes"])

    if "OGTT" in testDict.keys():
        if testDict["OGTT"] < 139: 
            kb.tell(OGTT["Normal"])
        else:
            if testDict["OGTT"] >= 140 and  testDict["OGTT"] <= 199:
                kb.tell(OGTT["Prediabetes"])
            else:
                kb.tell(OGTT["Diabetes"])

    if "RPG" in testDict.keys():
        if testDict["RPG"] >= 200: 
            kb.tell(RPG["Diabetes"])

    return (Score, kb)

def interpretResults(kb, diagnostic, Score):
    flag = False;

    if Score <= 40 and noTestsDone == False:
        print("The simptoms and riscs does not suport the keed for tests!") 

    if noTestsDone and diagnostic != "None":
        print("No definitive diagnostic can be given! Recomandation: do some tests.")       
    else:
        rez = kb.ask(Diabetes)
        if rez == {}:
            print("The correct diagnostic is: Diabetes.")
            flag = True

        rez = kb.ask(Prediabetes)
        if rez == {}:
            print("The correct diagnostic is: Prediabetes.")
            flag = True

        if flag == False:
            print("The correct diagnostic is: No diabetes.")

        print("Your diacnostic is: " + diagnostic)

    if len(IrelevantSimptoms) > 0:
        print("The following symptom(s) did not influence the decision:")
        for symptom in IrelevantSimptoms:
            print(symptom)

    if len(IrelevantRiscs) > 0:
        print("The following risk(s) did not influence the decision:")
        for risk in IrelevantRiscs:
            print(risk)

    if len(IrelevantTests) > 0:
        print("The following test(s) did not influence the decision:")
        for test in IrelevantTests:
            print(test)
    

def main():
    content = readDefaultInputFile()
    kb = InitKB()
    (simptomsList, riscsList, testDict, diagnostic) = parseContent(content)
    Score, kb = processData(simptomsList, riscsList, testDict, diagnostic, kb)
    interpretResults(kb, diagnostic, Score)

if __name__ == '__main__':
    main()