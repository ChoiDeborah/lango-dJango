# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import django
import sys

sys.path.append("/Users/deborah/Desktop/lango-django")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

#from lango-content.models import ModelName
from lango_content.models import Sentence
from lango_content.models import Pattern
from lango_content.models import PatternType
from lango_content.models import PatternCategory


if __name__ == "__main__":
    print(Sentence.objects.all())


def Load_XML(pathName):
    count = 0

    f = open(pathName, 'r')  # 읽는 모드로 파일을 열고
    string = ""  # isline, string 초기화
    isline = False

    while True:
        line = f.readline()  # 파일에서 한 라인을 읽어 라인에 저장

        if not line and not isline:  # 만약 라인이 NULL 값이면서 이전 라인 존재 시 브래이크
            break

        if isLine(line):    # 라인이 줄바꿈, 주석, 공백에 해당하지 않으면
            string += line  # string에 라인을 더해주고
            isline = True   # 라인상태 변수는 참

        else:  # 줄바꿈, 주석, 공백에 해당하면
            if isline:  # 만약 라인이냐가 트루일 때 만
                isline = False  # 라인상태변수는 거짓이 된다

        if not isline and not string == "":  # XML 파싱이 끝난지점인지 체크
            count = parse_String_To_XML(string, count)
            isline = False
            string = ""

    f.close()

    return count


# ----------------------------------------

def parse_String_To_XML(string, count):  # string -> XML

    root = ET.fromstring(string)  # string을 root에 넣고 파싱한다
    count += 1  # 문장 수 + 1
    #if searching(root, type):
    #print(type + "\n\n" + string + "\n")
    result = searching(root, type)

    if(result != "NO PATTERN"):
        print(string + "\n\n")

    #else:
    #    print(string+"\n")

    return count


# ----------------------------------------


def isLine(line):  # 줄바꿈 주석 공백 인지 체크 하는 함수
    if not line == '\n' and not line[:4] == '<!--' and not line == '':
        return True
    else:
        return False

# ----------------------------------------


def searching(node, type):

    result = "NO PATTERN"
    word_pos = ""
    pattern_1 = ""
    count = 0
    isNext = True

    for part in node.findall("part"):
        if isNext:
            count = 0
            pattern_1 = part_search(part, type, 1, word_pos)
            #반환되는 pattern이  be, sv, vb 일 경우 isWord = False

            if pattern_1 == "nn":        #반환되는 pattern이 nn 일 경우
                word_pos = "exist"
                pattern_2 = part_search(part, type, 1, word_pos)
                if pattern_2 == "nn":       # 명사구
                    result = "NN-100"
                elif pattern_2 == "J":      # 명사절
                    result = "NN-200"
                elif pattern_2 == "H":      # to부정사구
                    result = "NJ-100"
                elif pattern_2 == "N":      # 현재분사구
                    result = "NJ-200"
                elif pattern_2 == "P":      # 과거분사구
                    result = "NJ-300"
                elif pattern_2 == "R":      # 전치사구
                    result = "NJ-400"
                elif pattern_2 == "K":      # 형용사절
                    result = "NJ-500"
                if result != "NO PATTERN": print(result)

        if not isNext:
            if pattern_1 == "be":  # be동사구
                pattern_2 = part_search(part, type, 1, word_pos)
                if pattern_2 == "G":        # to부정사구
                    result = "BE-120"
                elif pattern_2 == "nn":     # 명사구
                    result = "BE-110"
                elif pattern_2 == "aj":     # 형용사구
                    result = "BE-210"
                elif pattern_2 == "M":      # 동명사구
                    result = "BE-130"
                elif pattern_2 == "J":      # 명사절
                    result = "BE-140"
                elif pattern_2 == "T":      # 원형부정사
                    result = "BE-150"
                elif pattern_2 == "R":      # 전치사구
                    result = "BE-220"
                elif pattern_2 == "N":      # 현재분사구
                    result = "BE-230"
                elif pattern_2 == "P":      # 과거분사구
                    result = "BE-240"
                if result != "NO PATTERN": print(result)
                

            # 상태동사
            elif pattern_1 == "sv":
                pattern_2 = part_search(part, type, 1, word_pos)
                if pattern_2 == "G":  # to부정사구
                    result = "SV-120"
                elif pattern_2 == "nn":  # 명사구
                    result = "SV-110"
                elif pattern_2 == "aj":  # 형용사구
                    result = "SV-210"
                elif pattern_2 == "M":  # 동명사구
                    result = "SV-130"
                elif pattern_2 == "J":  # 명사절
                    result = "SV-140"
                elif pattern_2 == "T":  # 원형부정사
                    result = "SV-150"
                elif pattern_2 == "R":  # 전치사구
                    result = "SV-220"
                elif pattern_2 == "N":  # 현재분사구
                    result = "SV-230"
                elif pattern_2 == "P":  # 과거분사구
                    result = "SV-240"
                if result != "NO PATTERN": print(result)

            # 일반동사구
            elif pattern_1 == "vb":
                pattern_2 = part_search(part, type, 1, word_pos)
                if pattern_2 == "G":        # to부정사구
                    result = "VB-120"
                elif pattern_2 == "nn":     # 명사구
                    result = "VB-110"
                elif pattern_2 == "M":      # 동명사구
                    result = "VB-130"
                elif pattern_2 == "J":      # 명사절
                    result = "VB-140"
                elif pattern_2 == "T":      #원형부정사
                    result = "VB-150"
                if result != "NO PATTERN":print(result)


        if pattern_1 == "be" or pattern_1 == "sv" or pattern_1 == "vb":
            isNext = False

        count += 1

    return result


# ----------------------------------------

def part_search(part, type, depth, pos):

    result = False

    # word pos 가 존재 할 때 (ex be동사구, 일반동사구, 상태동사구)
    if pos == "":
        for word in part.findall("word"):
            pos = word.get("pos")
            return pos

    # word pos 가 존재 하지 않을 때 (chunk일 때)
    for chunk in part.findall("chunk"):
        pos = chunk_search(chunk, type, depth)

        if pos != "NOT FOUND":
            return pos

    return pos


# ----------------------------------------

def chunk_search(chunk, type, depth):

    pattern = "NOT FOUND"

    chunk_pos = chunk.get("pos")

    result = False

    searching(chunk, "type")

    if chunk_pos == 'nn':
        # to부정사구 (G)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "", " to ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "G"
        # 동명사구 (M)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "M"

        # 명사절 (J)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ")
            elif result:
                #result = False
                if part_unit_check(part, "prd", "", ""):
                    return "J"

        # 원형부정사 (T)
        for part in chunk.findall("part"):
            if part_unit_check(part, "prd", "", ""):
                return "T"

    if chunk_pos == 'aj':
        # 전치사구 (R)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "pp", " ")
            elif result:
                result = False
                if part_unit_check(part, "obj", "", ""):
                    return "R"

        # 현재분사구 (N)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "N"

        # 과거분사구 (P)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbn", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "P"
        # 형용사절 (K)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "K"

        # to부정사구 (H)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "", " to ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "H"

    # 부사
    if chunk_pos == 'av':

        # to부정사구 (I)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "", " to ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "I"

        # 부사절(L)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "L"

        # 현재분사구 (O)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "O"

        # 과거분사구 (Q)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbn", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "Q"

            # 전치사구 (S)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "pp", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    return "S"

    return pattern
# ----------------------------------------


def part_unit_check(part, role, pos, text):

    result = False
    wordText = False
    part_role = part.get("role")

    if role == part_role:
        for word in part.findall("word"):
            wordText = True
            word_pos = word.get("pos")
            if pos == '':
                return True
            if word_pos == pos:
                word_text = word.text
                if word_text == text or text == " ":
                    return True
            # part안에 word가 존재 하지 않을 때
        if not wordText:
            return True

    return result
# ----------------------------------------

sum = 0

#for i in range(1, 13):  # 1 - 12 까지의 XML 불러오기
for i in range(0, 13):
    count = 0
    sum += Load_XML("/Users/deborah/Desktop/lango-django/lango_content/xml/" + str(i) + ".xml")  # Load_XML에 file Path를 인자로 전달 호출

print(sum)