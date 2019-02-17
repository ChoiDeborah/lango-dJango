# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

import nltk
#nltk.download('averaged_perceptron_tagger')
#nltk.download('all')

from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

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

    result = Searching(root)

    if result != "":
        print(str(count) + "\n" + string)
    else:
        print(str(count) + "\n" + string)

    return count


# ----------------------------------------


def isLine(line):  # 줄바꿈 주석 공백 인지 체크 하는 함수
    if not line == '\n' and not line[:4] == '<!--' and not line == '':
        return True
    else:
        return False


# ----------------------------------------

def Searching(_node):
    # xml Node 와, depth를 인자로 넘긴다.
    type = ""

    type = Part_Search(_node, 1)

    return type


# ----------------------------------------

def Part_Search(_node, _depth):

    chPattern_Of_Part = ""      # 파트의 패턴을 저장
    iCount_Part_Of_Num = 0    # 몇번째 파트인지 저장
    iCount_Part_Search = 0
    pattern = ""
    tempPattern =""
    bIsHead = False

    # 파트만큼 반복하고.
    # 파트 가 있다면 get_part_Pattern를 호출 하고
    # 몇번째 파트인지, 몇번째 댑스인지를 보낸다

    # 서술어 조건 일반동사인지 be동사인지 상태동사 인지 구분

    # 일반동사 일때
    # 1번째 part가 prd or trg 이면서 pos가 vb or vbn vbg이어야 한다.
    # 위 조건에 만족하면 2번째 파트의 role이 obj 이어야 한다.
    bResult = False
    for part in _node.findall("part"):

        if not bResult:
            chRole = "prd|trg"
            chPos = "vb|vbn|vbg"
            chWord = ""
            bResult = Part_Unit_Search(part, chRole, chPos, chWord)
        elif bResult and iCount_Part_Search == 0:
            bResult = False
            iCount_Part_Search += 1
            chRole = "obj"
            chPos = ""
            chWord = ""
            bResult = Part_Unit_Search(part, chRole, chPos, chWord)
            pattern = part_element_search(part, 1)
            if pattern == "nn":     # 명사구
                #print("-ON10")
                tempPattern = "-ON10"
            if pattern == "M":       # 동명사구
                #print("-ON20")
                tempPattern = "-ON20"
            if pattern == "G":      # 부정사구
                #print("-ON30")
                tempPattern = "-ON30"
            if pattern == "J":       # 명사절
                #print("-ON40")
                tempPattern = "-ON40"
            if pattern == "T":       # 원형 부정사
                #print("-ON50")
                tempPattern = "-ON50"

        elif bResult and iCount_Part_Search != 0:
            iCount_Part_Search += 1
            chRole = "!obj|!cpm"
            chPos = ""
            chWord = ""
            bResult = Part_Unit_Search(part, chRole, chPos, chWord)
            pattern = part_element_search(part, 1)

        iCount_Part_Of_Num += 1  # 파트 카운트 증가

    if iCount_Part_Search >= 1 and bResult:
        chPattern_Of_Part += "VB"
        chPattern_Of_Part += tempPattern
        #print("VB")
        print(chPattern_Of_Part)
        bIsHead = True

    # be동사 일 때
    # 첫번째 파트의 롤 prd|trg word pos 가 lemma(be)
    # 두번째 파트의 롤 cpm
    # 세번째 파트 존재 시 파트의 롤이 !obj|!cpm 이어야 한다.
    bResult = False
    iCount_Part_Of_Num = 0
    iCount_Part_Search = 0
    tempPattern = ""
    bIsHead = False
    for part in _node.findall("part"):
        #print(part.get("role"))
        if not bResult:
            chRole = "prd|trg"
            chPos = ""
            chWord = " lemma:be "
            bResult = Part_Unit_Search(part,  chRole, chPos, chWord)
        elif bResult and iCount_Part_Search == 0:
            bResult = False
            iCount_Part_Search += 1
            chRole = "cpm"
            chPos = ""
            chWord = ""
            bResult = Part_Unit_Search(part,  chRole, chPos, chWord)
            pattern = part_element_search(part, 1)
            if pattern == "nn": #명사구
                #print("-CN10")
                tempPattern = "-CN10"
            if pattern == "M":  #동명사구
                #print("-CN20")
                tempPattern = "-CN20"
            if pattern == "G":  #to부정사구
                #print("-CN30")
                tempPattern = "-CN30"
            if pattern == "J":  #명사절
                #print("-CN40")
                tempPattern = "CN40"
            if pattern == "T":  #원형부정사
                #print("-CN50")
                tempPattern = "-CN50"
            if pattern == "aj": #형용사구
                #print("-CJ10")
                tempPattern = "-CJ10"
            if pattern == "R":  #전치사구
                #print("-CJ20")
                tempPattern = "-CJ20"
            if pattern == "N":  #현재 분사구
                #print("-CJ30")
                tempPattern = "-CJ30"
            if pattern == "P":  #과거 분사구
                #print("-CJ40")
                tempPattern = "-CJ40"

        elif bResult and iCount_Part_Search != 0:
            iCount_Part_Search += 1
            chRole = "!obj|!cpm"
            chPos = ""
            chWord = ""
            bResult = Part_Unit_Search(part,  chRole, chPos, chWord)
        iCount_Part_Of_Num += 1  # 파트 카운트 증가

    if iCount_Part_Search >= 1 and bResult:
        chPattern_Of_Part += "BE"
        chPattern_Of_Part += tempPattern
        #print("BE")
        print(chPattern_Of_Part)
        bIsHead = True


    # 상태동사
    # 1 part role = prd|trg text = !lemma(be)
    # 2 part role = cpm
    bResult = False
    iCount_Part_Of_Num = 0
    iCount_Part_Search = 0
    tempPattern = ""
    bIsHead = False
    for part in _node.findall("part"):
        if not bResult:
            chRole = "prd|trg"
            chPos = ""
            chWord = " !lemma:be "
            bResult = Part_Unit_Search(part,  chRole, chPos, chWord)
        elif bResult:
            bResult = False
            iCount_Part_Search += 1
            chRole = "cpm"
            chPos = ""
            chWord = ""
            bResult = Part_Unit_Search(part,  chRole, chPos, chWord)
            pattern = part_element_search(part, 1)
            if pattern == "nn":  # 명사구
                #print("-CN10")
                tempPattern = "-CN10"
            if pattern == "M":  # 동명사구
                #print("-CN20")
                tempPattern = "-CN20"
            if pattern == "G":  # to부정사구
                #print("-CN30")
                tempPattern = "-CN30"
            if pattern == "J":  # 명사절
                #print("-CN40")
                tempPattern = "-CN40"
            if pattern == "T":  # 원형부정사
                #print("-CN50")
                tempPattern = "-CN50"
            if pattern == "aj":  # 형용사구
                #print("-CJ10")
                tempPattern = "-CJ10"
            if pattern == "R":  # 전치사구
                #print("-CJ20")
                tempPattern = "-CJ20"
            if pattern == "N":  # 현재 분사구
                #print("-CJ30")
                tempPattern = "-CJ30"
            if pattern == "P":  # 과거 분사구
                #print("-CJ40")
                tempPattern = "-CJ40"
        elif bResult and iCount_Part_Search > 1:
            iCount_Part_Search += 1
            chRole = "!obj|!cpm"
            chPos = ""
            chWord = ""
            bResult = Part_Unit_Search(part, chRole, chPos, chWord)
        iCount_Part_Of_Num += 1  # 파트 카운트 증가

    if iCount_Part_Search >= 1 and bResult:
        chPattern_Of_Part += "SV"
        chPattern_Of_Part += tempPattern
        #print("SV")
        print(chPattern_Of_Part)
        bIsHead = True


    return  chPattern_Of_Part
# ----------------------------------------

def part_element_search(_part, _depth):
    result = False
    wordText = False
    pos = ""
    # word pos 가 존재 할 때 (ex be동사구, 일반동사구, 상태동사구)

    chunkText = False

    # word 존재 시
    for word in _part.findall("word"):
        wordText = True
        pos = word.get("pos")
        return pos

    # word pos 가 존재 하지 않을 때 (chunk일 때)
    for chunk in _part.findall("chunk"):
        pos = chunk_search(chunk, _depth)
        print("(")
        Part_Search(chunk, _depth+1)
        print(")")
        if pos != "":
            return pos

    return pos

# ----------------------------------------

def chunk_search(chunk,  depth):
    pattern = ""

    chunk_pos = chunk.get("pos")

    result = False

    if chunk_pos == 'nn':
        # to부정사구 (G)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "", " to ")
            elif result:
                result = False
                if Part_Unit_Search(part, "prd", "", ""):
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "G"
        # 동명사구 (M)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "vbg", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "prd", "", ""):
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "M"

        # 명사절 (J)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "cj", " ")
            elif result:
                # result = False
                if Part_Unit_Search(part, "", "", ""):
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "J"

        # 원형부정사 (T)
        for part in chunk.findall("part"):
            if Part_Unit_Search(part, "prd", "", ""):
                #for tempChunk in part.findall("chunk"):
                    #if depth <= 2:
                        #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                return "T"

    if chunk_pos == 'aj':
        # 전치사구 (R)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "pp", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "obj", "", ""):
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "R"

        # 현재분사구 (N)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "vbg", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "", "", ""):
                   # for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "N"

        # 과거분사구 (P)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "vbn", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "", "", ""):
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "P"
        # 형용사절 (K)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "cj", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "", "", ""):
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "K"

        # to부정사구 (H)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "", " to ")
            elif result:
                result = False
                if Part_Unit_Search(part, "prd", "", ""):
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "H"

    # 부사
    if chunk_pos == 'av':

        # to부정사구 (I)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "", " to ")
            elif result:
                result = False
                if Part_Unit_Search(part, "prd", "", ""):
                    return "I"
                    pattern = "I"
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

        # 부사절(L)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "cj", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "", "", ""):
                    return "L"
                    #pattern = "L"
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

        # 현재분사구 (O)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "vbg", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "", "", ""):
                    return "O"
                    #pattern = "O"
                    #for tempChunk in part.findall("chunk"):
                        #if depth <=2 :
                            #print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

        # 과거분사구 (Q)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "vbn", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "", "", ""):
                    return "Q"
                    #pattern = "Q"
                    #for tempChunk in part.findall("chunk"):
                    #    if depth <=2 :
                    #        print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

            # 전치사구 (S)
        for part in chunk.findall("part"):
            if not result:
                result = Part_Unit_Search(part, "trg", "pp", " ")
            elif result:
                result = False
                if Part_Unit_Search(part, "obj", "", ""):
                    return "S"
                    #pattern = "S"
                    #for tempChunk in part.findall("chunk"):
                    #    if depth <=2 :
                    #        print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

        return pattern

    return pattern

# -----------------------------------

def Part_Unit_Search(_part,_role, _pos, _text):
    bResult = False

    result = False
    wordText = False

    # part 는 xml
    # role , pos, text 비교 대상

    # role에 or 있는지 확인
    indexOr = _role.find("|")

    # if or 있으면
    if indexOr != -1:
        role_1 = _role[0:indexOr]  # role_1 에 role or 전까지 저장
        if role_not_check(_part, role_1, _pos, _text):
            return True
        role_2 = _role[indexOr + 1:]  # role_2 에 role or 후부터 저장
        if role_not_check(_part, role_2, _pos, _text):
            return True

    # if or 없으면
    if indexOr == -1:
        if role_not_check(_part, _role, _pos, _text):
            return True

    return bResult

# ---------------------------------------

def role_not_check(_part, _role, _pos, _text):
    bResult = False
    wordText = False

    xml_part_role = _part.get("role")

    # _pos에 find 확인
    indexOr  = _pos.find("|")

    pos_1 = ""
    pos_2 = ""
    pos_3 = ""

    if indexOr != -1:
        pos_1 = _pos[0:indexOr]  # role_1 에 role or 전까지 저장
        tempPos = _pos[indexOr + 1:]  # role_2 에 role or 후부터 저장
        indexOr = tempPos.find("|")
        if indexOr == -1:
            pos_2 = tempPos
        elif indexOr != -1:
            pos_2 = tempPos[0:indexOr]
            pos_3 = tempPos[indexOr+1:]
    elif indexOr == -1:
        pos_1 = _pos

    if _role[:1] == "!":  # role앞에 !일 때
        role = _role[1:]  # ! 떼고 role에 저장
        if xml_part_role != role:

            for word in _part.findall("word"):
                wordText = True
                xml_word_pos = word.get("pos")
                if xml_word_pos == pos_1 or xml_word_pos == pos_2 or xml_word_pos == pos_3 or _pos == "":
                    xml_word_text = word.text
                    if _text == " " or xml_word_text == _text or _text == "":
                        return True

                    if _text == " !lemma:be ":
                        lemma_text = wordnet_lemmatizer.lemmatize(xml_word_text, pos="v")
                        if lemma_text != "be":
                            return True
                    elif _text == " lemma:be ":
                        lemma_text = wordnet_lemmatizer.lemmatize(xml_word_text, pos="v")
                        if lemma_text == "be":
                            return True

            if not wordText:
                return True

    else:  # if role에 ! 없으면
        if xml_part_role == _role or _role == "":

            for word in _part.findall("word"):
                wordText = True
                xml_word_pos = word.get("pos")

                if xml_word_pos == pos_1 or xml_word_pos == pos_2 or xml_word_pos == pos_3 or _pos == "":
                    xml_word_text = word.text
                    if _text == " " or xml_word_text == _text or _text == "":
                        return True

                    if _text == " !lemma:be ":
                        xml_word_text = xml_word_text[1:-1]
                        lemma_text = wordnet_lemmatizer.lemmatize(xml_word_text, pos="v")
                        if lemma_text != "be":
                            return True

                    elif _text == " lemma:be ":
                        xml_word_text = xml_word_text[1:-1]
                        lemma_text = wordnet_lemmatizer.lemmatize(xml_word_text, pos="v")
                        if lemma_text == "be":
                            return True

            if not wordText:
                return True

    return bResult

# for i in range(1, 13):  # 1 - 12 까지의 XML 불러오기
#for i in range(0, 13):
#    count = 0
#    sum += Load_XML("/Users/deborah/Desktop/Detecting/xml/" + str(i) + ".xml")  # Load_XML에 file Path를 인자로 전달 호출
Load_XML("/Users/deborah/Desktop/Detecting/xml/0.xml")  # Load_XML에 file Path를 인자로 전달 호출

#print(sum)