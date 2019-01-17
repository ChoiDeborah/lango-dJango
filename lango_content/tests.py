from django.test import TestCase

# Create your tests here.
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import django
import sys

sys.path.append('/Users/deborah/Desktop/lango-django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

#from yourapp.models import your_model

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

        if isLine(line):  # 라인이 줄바꿈, 주석, 공백에 해당하지 않으면
            string += line  # string에 라인을 더해주고
            isline = True  # 라인상태 변수는 참

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

    # BE-110 / BE-120 / VB-100 / 전치사-to / to부정사
    type = "BE-110"
    # type = "BE-120"
    # type = "VB-100"
    # type = "전치사-to"
    # type = "to부정사"
    #type = "명사+전치사-to"

    if searching(root, type):
        print(type + "\n\n" + string)
        PatternType.objects.create(pattern_type='BE-130')
        #PatternCategory.objects.create("수식")
        #a =
        #Sentence.objects.create(sentence='I am a boy', article='aaa', released_date='2018-12-12 12:00:00', xml=string, pattern=Pattern.objects.create(pattern_Type_id=1, Pattern_Category_id=1))

    else:
        print("False\n")

    return count



# ----------------------------------------


# ----------------------------------------

def isLine(line):  # 줄바꿈 주석 공백 인지 체크 하는 함수
    if not line == '\n' and not line[:4] == '<!--' and not line == '':
        return True
    else:
        return False

    # ----------------------------------------


def searching(node, type):
    result = False

    if type == "BE-110":
        for part in node.findall("part"):

            if not result:  # result 가 False 일 때
                result = part_search(part, "prd", "be", 1, 0, type, "")

            else:  # result가 True 가 되면
                result = False
                result = part_search(part, "cpm", "nn", 1, 0, type, "")
                if result:
                    return True

    if type == "BE-120":
        for part in node.findall("part"):
            if not result:
                result = part_search(part, "prd", "be", 1, 0, type, "")

            else:
                result = False
                result = part_search(part, "cpm", "", 1, 1, type, "")  #  chunk가 존재하는 경우
                if result:
                    return True

    if type == "VB-100":
        for part in node.findall("part"):
            if not result:
                result = part_search(part, "prd", "vb", 1, 0, type, "")
            else:
                result = False
                result = part_search(part, "obj", "nn", 1, 1, type, "")
                if result:
                    return True

    if type == "전치사-to":
        for part in node.findall("part"):
            if not result:
                result = part_search(part, "", "", 1, 1, type, "")
                if (result):
                    return True

    if type == "to부정사":
        for part in node.findall("part"):
            if not result:
                result = part_search(part, "", "", 1, 1, type, "")
                if (result):
                    return True

    if type == "명사+전치사-to":
        for part in node.findall("part"):
            if not result:
                result = part_search(part, "", "nn", 1, 3, type, "")  # part안에 word, chunk 올 때
                if (result):
                    return True

    # if type == "명사+to부정사":
    #    for part in node.findall("part"):
    #        if not result:
    #            result = part_search(part, "" )

    return False


# ----------------------------------------

def part_search(part, role_keyword, pos_keyword, depth, isChunk, type, text):
    result = False

    role = part.get("role")  # if 파트의 롤과 매개변수로 받은 롤을 비교
    chunkText = False

    #### 명사 + 전치사 to
    # if isChunk == 3:                            # word, chunk 올 때 isChunk == 3
    #    for word in part.findall("word"):   # word 를 순회한다
    #        wordPos = word.get("pos")           # word의 pos를 가져온다
    #        if wordPos == "nn":                 # 만약 pos 가 "nn"이면
    #            for chunk in part.findall("chunk"):
    #
    #            break

    if isChunk == 2:  # word 나 chunk나 상관 없을 때
        if (role_keyword[:1] == "!"):  # role_keyword 만 제외하고
            roleTemp = role_keyword[1:]  # !제외한 나머지 문자열 슬라이싱
            if roleTemp == "obj":
                if role != roleTemp:  # roleTemp 제외한 나머지 일 경우
                    return True
        elif role == role_keyword:
            return True

    if isChunk == 0:  # word 비교 시
        for chunk in part.findall("chunk"):  # chunk가 존재 하면
            return False  # False 반환
        if (role == role_keyword or role_keyword == ""):
            for word in part.findall("word"):
                pos = word.get("pos")
                if pos == pos_keyword or pos_keyword == "":  # 같으면 word의 pos 비교
                    if text == "":  # word 의 text 가 ""이거나 같을 때
                        return True
                    elif word.text == text:
                        return True

        elif (role_keyword[:1] == "!"):  # role_keyword 만 제외하고
            roleTemp = role_keyword[1:]  # !제외한 나머지 문자열 슬라이싱
            if roleTemp == "obj":
                if role != roleTemp:  # roleTemp 제외한 나머지 일 경우
                    for word in part.findall("word"):
                        pos = word.get("pos")
                        if pos == pos_keyword or pos_keyword == "":  # 같으면 word의 pos 비교
                            if text == "":  # word 의 text 가 ""이거나 같을 때
                                return True
                            elif word.text == text:
                                return True

    if isChunk == 1:  # Chunk 비교 시
        for word in part.findall("word"):  # word 가 존재하면
            return False  # False 반환
        if (role == role_keyword or role_keyword == ""):
            for chunk in part.findall("chunk"):
                pos = chunk.get("pos")
                if pos == pos_keyword or pos_keyword == "":
                    if (type == "BE-120"):
                        role_keyword = "trg"
                        pos_keyword = ""
                        text = " to "
                    if (type == "VB-100"):
                        role_keyword = "trg"
                        pos_keyword = "cj"
                    if (type == "전치사-to"):
                        role_keyword = "trg"
                        pos_keyword = ""
                        text = " to "
                    if (type == "to부정사"):
                        role_keyword = "trg"
                        pos_keyword = ""
                        text = " to "
                    result = chunk_search(chunk, depth, role_keyword, pos_keyword, type, text)
                    if result:
                        return True

    return result


# ----------------------------------------

def chunk_search(chunk, depth, role_keyword, pos_keyword, type, text):
    result = False

    if type == "BE-120":
        for part in chunk.findall("part"):
            if not result:
                result = part_search(part, role_keyword, pos_keyword, depth + 1, 0, type,
                                     " to ")  # word.text가 " to " 일 때 참

            else:
                result = False
                result = part_search(part, "!obj", "", depth + 1, 0, type, "")  # role이 obj가 아닌 것 만
                if result:
                    return True

    elif type == "전치사-to":
        for part in chunk.findall("part"):
            if not result:
                result = part_search(part, role_keyword, pos_keyword, depth + 1, 0, type, " to ")
            else:
                result = False
                result = part_search(part, "obj", "", depth + 1, 2, type, "")
                if result:
                    return True

    elif type == "to부정사":
        for part in chunk.findall("part"):
            if not result:
                result = part_search(part, role_keyword, pos_keyword, depth + 1, 0, type, " to ")
            else:
                result = False
                result = part_search(part, "!obj", "", depth + 1, 2, type, "")
                if result:
                    return True


    else:
        for part in chunk.findall("part"):
            result = part_search(part, role_keyword, pos_keyword, depth + 1, 0, type, text)
            if result:
                return True

    return result


# ----------------------------------------

sum = 0

for i in range(1, 13):  # 1 - 12 까지의 XML 불러오기
    count = 0
    sum += Load_XML("/Users/deborah/Desktop/Sentence_Scoring/xml/" + str(i) + ".xml")  # Load_XML에 file Path를 인자로 전달 호출

print(sum)