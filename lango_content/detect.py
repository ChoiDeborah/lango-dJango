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

    result = searching(root, 1)
    if (result != "NO PATTERN"):
       print(string + "\n\n")

    return count


# ----------------------------------------


def isLine(line):  # 줄바꿈 주석 공백 인지 체크 하는 함수
    if not line == '\n' and not line[:4] == '<!--' and not line == '':
        return True
    else:
        return False


# ----------------------------------------

def searching(node, depth):

    result = False
    vbResult = False
    count = 0
    partCount = 0
    type = ""

    # be동사
    for part in node.findall("part"):
        if(not result):
            result = part_unit_check(part, "prd|trg", "", " lemma:be ")
        if result:
            #print("BE")
            pattern_2 = part_search(part, depth)
            if pattern_2 == "G":  # to부정사구
                print("BE-CN30")
                type = "BE-CN30"
            elif pattern_2 == "nn":  # 명사구
                print("BE-CN10")
                type = "BE-CN10"
            elif pattern_2 == "aj":  # 형용사구
                print("BE-CJ10")
                type = "BE-CJ10"
            elif pattern_2 == "M":  # 동명사구
                print("BE-CN20")
                type = "BE-CN20"
            elif pattern_2 == "J":  # 명사절
                print("BE-CN40")
                type = "BE-CN40"
            elif pattern_2 == "T":  # 원형부정사
                print("BE-CN35")
                type = "BE-CN35"
            elif pattern_2 == "R":  # 전치사구
                print("BE-CJ20")
                type = "BE-CJ20"
            elif pattern_2 == "N":  # 현재분사구
                print("BE-CJ30")
                type = "BE-CJ30"
            elif pattern_2 == "P":  # 과거분사구
                print("BE-CJ40")
                type = "BE-CJ40"

    # 일반동사
    for part in node.findall("part"):
        if not result and count == 1:
            vbResult = part_unit_check(part, "obj", "", " ")
        count += 1
        if(vbResult):
            pattern_2 = part_search(part, depth)
            if pattern_2 == "G": # to부정사
                print("VB-ON30")
                type = "VB-ON30"
                break
            elif pattern_2 == "J": # 명사절
                print("VB-ON40")
                type = "VB-ON40"
                break
            elif pattern_2 == "T": # 원형부정사
                print("VB-ON50")
                type = "VB-ON50"
                break
            elif pattern_2 == "M": # 동명사구 뒤에 청크온다
                print("VB-ON20")
                for tempChunk in part.findall("chunk"):
                    pattern_3 = chunk_search(tempChunk, depth+1)
                    if pattern_3 == "nn":  # 명사구
                        print("CN10")
                    elif pattern_3 == "M":  # 동명사구
                        print("CN20")
                    elif pattern_3 == "G":  # to부정사구
                        print("CN30")
                    elif pattern_3 == "J":  # 명사절
                        print("CN40")
                    elif pattern_3 == "T":  # 원형부정사
                        print("CN50")
                    # aj 형용사 보어
                    elif pattern_3 == "K":  # 형용사구
                        print("CJ10")
                    elif pattern_3 == "R":  # 전치사구
                        print("CJ20")
                    elif pattern_3 == "N":  # 현재분사구
                        print("CJ30")
                    elif pattern_3 == "P":  # 과거분사구
                        print("CJ40")
                    elif pattern_3 == "H":  # to부정사
                        print("CJ50")
                type = "VB-ON20"
                break
            elif pattern_2 =="nn": # 명사구 뒤에 청크 온다
                print("VB-ON10")
                for tempChunk in part.findall("chunk"):
                    pattern_3 = chunk_search(tempChunk, depth + 1)
                    if pattern_3 == "nn":  # 명사구
                        print("CN10")
                    elif pattern_3 == "M":  # 동명사구
                        print("CN20")
                    elif pattern_3 == "G":  # to부정사구
                        print("CN30")
                    elif pattern_3 == "J":  # 명사절
                        print("CN40")
                    elif pattern_3 == "T":  # 원형부정사
                        print("CN50")
                        # aj 형용사 보어
                    elif pattern_3 == "K":  # 형용사구
                        print("CJ10")
                    elif pattern_3 == "R":  # 전치사구
                        print("CJ20")
                    elif pattern_3 == "N":  # 현재분사구
                        print("CJ30")
                    elif pattern_3 == "P":  # 과거분사구
                        print("CJ40")
                    elif pattern_3 == "H":  # to부정사
                        print("CJ50")
                type = "VB-ON10"
                break
            else:
                print("VB-ELSE")
                type = "VB-ELSE"
                break
        partCount += 1

    # 상태동사
    for part in node.findall("part"):
        if not result and not vbResult:
            result = part_unit_check(part, "prd|trg", "", " !lemma:be ")
            #if result: print("VB")
        if result:
            #print("SV")
            pattern_2 = part_search(part, depth)
            if pattern_2 == "G":  # to부정사구
                print("SV-CN30")
                type = "SV-CN30"
            elif pattern_2 == "nn":  # 명사구
                print("SV-CN10")
                type = "SV-CN10"
            elif pattern_2 == "aj":  # 형용사구
                print("SV-CJ10")
                type = "SV-CJ10"
            elif pattern_2 == "M":  # 동명사구
                print("SV-CN20")
                type = "SV-CN20"
            elif pattern_2 == "J":  # 명사절
                print("SV-CN40")
                type = "SV-CN40"
            elif pattern_2 == "T":  # 원형부정사
                print("SV-CN35")
                type = "SV-CN35"
            elif pattern_2 == "R":  # 전치사구
                print("SV-CJ20")
                type = "SV-CJ20"
            elif pattern_2 == "N":  # 현재분사구
                print("SV-CJ30")
                type = "SV-CJ30"
            elif pattern_2 == "P":  # 과거분사구
                print("SV-CJ40")
                type = "SV-CJ40"

    # 명사구(수식)
    for part in node.findall("part"):
        if(not result and not vbResult):
            #result = part_unit_check(part, "", "nn", " ")
            for word in part.findall("word"):
                pos = word.get("pos")
                if pos == "nn":
                    result = True
        if result:
            for chunk in part.findall("chunk"):
                pattern_2 = chunk_search(chunk, depth+1)
                # nn 명사보어
                if pattern_2 == "nn":    # 명사구
                    print("NN-CN10")
                    type = "NN-CN10"
                elif pattern_2 == "M":  # 동명사구
                    print("NN-CN20")
                    type = "NN-CN2"
                elif pattern_2 == "G":  # to부정사구
                    print("NN-CN30")
                    type = "NN-CN30"
                elif pattern_2 == "J":  # 명사절
                    print("NN-CN40")
                    type = "NN-CN40"
                elif pattern_2 == "T":  # 원형부정사
                    print("NN-CN50")
                    type = "NN-CN50"
                # aj 형용사 보어
                elif pattern_2 == "K":  # 형용사구
                    print("NN-CJ10")
                    type = "NN-CJ10"
                elif pattern_2 == "R":  # 전치사구
                    print("NN-CJ20")
                    type = "NN-CJ20"
                elif pattern_2 == "N":  # 현재분사구
                    print("NN-CJ30")
                    type = "NN-CJ30"
                elif pattern_2 == "P":  # 과거분사구
                    print("NN-CJ40")
                    type = "NN-CJ400"
                elif pattern_2 == "H":  # to부정사
                    print("NN-CJ50")
                    type = "NN-CJ50"



    return type


# ----------------------------------------

def part_unit_check(part, role, pos, text):

    result = False
    wordText = False

    # part 는 xml
    # role , pos, text 비교 대상

    # role에 or 있는지 확인
    indexOr = role.find("|")

    # if or 있으면
    if indexOr != -1:
        role_1 = role[0:indexOr]      # role_1 에 role or 전까지 저장
        if role_not_check(part, role_1, pos, text):
            return True
        role_2 = role[indexOr+1:]     # role_2 에 role or 후부터 저장
        if role_not_check(part, role_2, pos, text):
            return True

    # if or 없으면
    if indexOr == -1:
        if role_not_check(part, role, pos, text):
            return True

    return result

# ----------------------------------------


def role_not_check(part, role, pos, text):
    result = False
    wordText = False

    xml_part_role = part.get("role")

    if role[:1] == "!":  # role앞에 !일 때
        role = role[1:]  # ! 떼고 role에 저장
        if xml_part_role != role:

            for word in part.findall("word"):
                wordText = True
                xml_word_pos = word.get("pos")

                if xml_word_pos == pos or pos == "":
                    xml_word_text = word.text
                    if text == " " or xml_word_text == text or text == "":
                        return True

                    if text == " !lemma:be ":
                        lemma_text = wordnet_lemmatizer.lemmatize(xml_word_text, pos="v")
                        if lemma_text != "be":
                            return True
                    elif text == " lemma:be ":
                        lemma_text = wordnet_lemmatizer.lemmatize(xml_word_text, pos="v")
                        if lemma_text == "be":
                            return True

            if not wordText:
                return True

    else:  # if role에 ! 없으면
        if xml_part_role == role or role == "":

            for word in part.findall("word"):
                wordText = True
                xml_word_pos = word.get("pos")

                if xml_word_pos == pos or pos == "":
                    xml_word_text = word.text
                    if text == " " or xml_word_text == text or text == "":
                        return True

                    if text == " !lemma:be ":
                        xml_word_text = xml_word_text[1:-1]
                        lemma_text = wordnet_lemmatizer.lemmatize(xml_word_text, pos="v")
                        if lemma_text != "be":
                            return True

                    elif text == " lemma:be ":
                        xml_word_text = xml_word_text[1:-1]
                        lemma_text = wordnet_lemmatizer.lemmatize(xml_word_text, pos="v")
                        if lemma_text == "be":
                            return True

            if not wordText:
                return True

    return result


# ----------------------------------------

def part_search(part, depth):
    result = False
    wordText = False
    pos = ""
    # word pos 가 존재 할 때 (ex be동사구, 일반동사구, 상태동사구)

    chunkText = False

    # word 존재 시
    for word in part.findall("word"):
        wordText = True
        pos = word.get("pos")
        return pos

    # word pos 가 존재 하지 않을 때 (chunk일 때)
    for chunk in part.findall("chunk"):
        pos = chunk_search(chunk, depth)

        if pos != "NOT FOUND":
            return pos

    return pos


# ----------------------------------------

def chunk_search(chunk,  depth):
    pattern = "NOT FOUND"

    chunk_pos = chunk.get("pos")

    result = False

    if chunk_pos == 'nn':
        # to부정사구 (G)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "", " to ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "G"
        # 동명사구 (M)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "M"

        # 명사절 (J)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ")
            elif result:
                # result = False
                if part_unit_check(part, "", "", ""):
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "J"

        # 원형부정사 (T)
        for part in chunk.findall("part"):
            if part_unit_check(part, "prd", "", ""):
                for tempChunk in part.findall("chunk"):
                    if depth <= 2:
                        print("(" + chunk_search(tempChunk, depth + 1) + ")")
                return "T"

    if chunk_pos == 'aj':
        # 전치사구 (R)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "pp", " ")
            elif result:
                result = False
                if part_unit_check(part, "obj", "", ""):
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "R"

        # 현재분사구 (N)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ")
            elif result:
                result = False
                if part_unit_check(part, "", "", ""):
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "N"

        # 과거분사구 (P)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbn", " ")
            elif result:
                result = False
                if part_unit_check(part, "", "", ""):
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "P"
        # 형용사절 (K)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ")
            elif result:
                result = False
                if part_unit_check(part, "", "", ""):
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    return "K"

        # to부정사구 (H)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "", " to ")
            elif result:
                result = False
                if part_unit_check(part, "prd", "", ""):
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
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
                    #return "I"
                    pattern = "I"
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

        # 부사절(L)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ")
            elif result:
                result = False
                if part_unit_check(part, "", "", ""):
                    #return "L"
                    pattern = "L"
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

        # 현재분사구 (O)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ")
            elif result:
                result = False
                if part_unit_check(part, "", "", ""):
                    #return "O"
                    pattern = "O"
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

        # 과거분사구 (Q)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbn", " ")
            elif result:
                result = False
                if part_unit_check(part, "", "", ""):
                    #return "Q"
                    pattern = "Q"
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

            # 전치사구 (S)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "pp", " ")
            elif result:
                result = False
                if part_unit_check(part, "obj", "", ""):
                    #return "S"
                    pattern = "S"
                    for tempChunk in part.findall("chunk"):
                        if depth <=2 :
                            print("(" + chunk_search(tempChunk, depth + 1) + ")")
                    break

        return pattern




    return pattern




# ----------------------------------------

sum = 0


# for i in range(1, 13):  # 1 - 12 까지의 XML 불러오기
for i in range(0, 13):
    count = 0
    sum += Load_XML("/Users/deborah/Desktop/Detecting/xml/" + str(i) + ".xml")  # Load_XML에 file Path를 인자로 전달 호출
#sum += Load_XML("/Users/deborah/Desktop/Detecting/xml/" + "0" + ".xml")  # Load_XML에 file Path를 인자로 전달 호출

#print(sum)