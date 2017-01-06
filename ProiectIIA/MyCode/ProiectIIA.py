import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
print(parentdir)
sys.path.insert(0,parentdir) 

if sys.version_info < (3, 0):
    raise "must use python 3.4 or greater"

from utils import *
from logic import *

Sex = {}
Sex['M'] = Symbol("Sex[M]")
Sex['F'] = Symbol("Sex[F]")

Age = {}
Age['49_L'] = Symbol("Age[49_L]")
Age['50_59'] = Symbol("Age[50_59]")
Age['60_69'] = Symbol("Age[60_69]")
Age['70_O'] = Symbol("Age[70_O]")

EthincBack = {}
EthincBack['White_Europ'] = Symbol("EthincBack[White_Europ]")
EthincBack['Other'] = Symbol("EthincBack[Other]")

History = {}
History['yes'] = Symbol("History[yes]")
History['no'] = Symbol("History[no]")

Waist = {}
Waist['90_L'] = Symbol("Waist[90_L]")
Waist['90_99'] = Symbol("Waist[90_99]")
Waist['100_109'] = Symbol("Waist[100_109]")
Waist['110_G'] = Symbol("Waist[110_G]")

BMI = {}
BMI['25_L'] = Symbol("BMI[25_L]")
BMI['25_29'] = Symbol("BMI[25_29]")
BMI['30_35'] = Symbol("BMI[30_35]")
BMI['35_O'] = Symbol("BMI[35_O]")

Medication = {}
Medication['yes'] = Symbol("Medication[yes]")
Medication['no'] = Symbol("Medication[no]")

diabetes = {}
diabetes['yes'] = Symbol("Diabetes[yes]")
diabetes['no'] = Symbol("Diabetes[no]")

def InitKB():
    kb = PropKB()

    kb.tell(Sex['M'])
    kb.tell(EthincBack['White_Europ'])
    kb.tell(Sex['M'] | '==>' | ~Sex['F'])
    kb.tell(Sex['F'] | '==>' | ~Sex['M'])
    kb.tell(Sex['M'] & EthincBack['White_Europ'] | '==>' | diabetes['yes'])

    return kb


def askKB(kb):
    rez = kb.ask(Sex['M'])
    if rez == {}:
        print("The pacient is male!")

    rez = kb.ask(~Sex['F'])
    if rez == {}:
        print("The pacient is not female!")

    rez = kb.ask(diabetes['yes'])
    if rez == {}:
        print("The pacient has diabetes!")
    else:
        print("The pacient does not have diabetes!")

def main():
    askKB(InitKB())

if __name__ == '__main__':
    main()