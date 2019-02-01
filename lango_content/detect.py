# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
#nltk.download('averaged_perceptron_tagger')
#nltk.download('all')
porter_stemmer = PorterStemmer()
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

    result = searching(root, type)
    if (result != "NO PATTERN"):
       print(string + "\n\n")

    # else:
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


    pattern = get_pattern(node)




    return type


# ----------------------------------------
def get_pattern(node):

    result = False
    vbResult = False
    count = 0

    # be동사
    for part in node.findall("part"):
        if(not result):
            result = part_unit_check(part, "prd|trg", "", " lemma:be ")
        if result:
            #print("BE")
            pattern_2 = part_search(part, 1)
            if pattern_2 == "G":  # to부정사구
                print("BE-CN30")
            elif pattern_2 == "nn":  # 명사구
                print("BE-CN10")
            elif pattern_2 == "aj":  # 형용사구
                print("BE-CJ10")
            elif pattern_2 == "M":  # 동명사구
                print("BE-CN20")
            elif pattern_2 == "J":  # 명사절
                print("BE-CN40")
            elif pattern_2 == "T":  # 원형부정사
                print("BE-CN35")
            elif pattern_2 == "R":  # 전치사구
                print("BE-CJ20")
            elif pattern_2 == "N":  # 현재분사구
                print("BE-CJ30")
            elif pattern_2 == "P":  # 과거분사구
                print("BE-CJ40")



    # 일반동사
    for part in node.findall("part"):
        if not result and count == 1:
            vbResult = part_unit_check(part, "obj", "", " ")
        count += 1
        if(vbResult):
            pattern_2 = part_search(part,1)
            if pattern_2 == "G": # to부정사
                print("VB-ON30")
                break
            elif pattern_2 == "J": # 명사절
                print("VB-ON40")
                break
            elif pattern_2 == "T": # 원형부정사
                print("VB-ON50")
                break
            elif pattern_2 == "M": # 동명사구 뒤에 청크온다
                print("VB-ON20")
                break
            elif pattern_2 =="nn": # 명사구 뒤에 청크 온다
                print("VB-ON10")
                break
            else:
                print("VB-ELSE")
                break


    # 상태동사
    for part in node.findall("part"):
        if not result and not vbResult:
            result = part_unit_check(part, "prd|trg", "", " !lemma:be ")
            #if result: print("VB")
        if result:
            #print("SV")
            pattern_2 = part_search(part, 1)
            if pattern_2 == "G":  # to부정사구
                print("SV-CN30")
            elif pattern_2 == "nn":  # 명사구
                print("SV-CN10")
            elif pattern_2 == "aj":  # 형용사구
                print("SV-CJ10")
            elif pattern_2 == "M":  # 동명사구
                print("SV-CN20")
            elif pattern_2 == "J":  # 명사절
                print("SV-CN40")
            elif pattern_2 == "T":  # 원형부정사
                print("SV-CN35")
            elif pattern_2 == "R":  # 전치사구
                print("SV-CJ20")
            elif pattern_2 == "N":  # 현재분사구
                print("SV-CJ30")
            elif pattern_2 == "P":  # 과거분사구
                print("SV-CJ40")

    #return type

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
                    if text == " " or xml_word_text == text:
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
                    if text == " " or xml_word_text == text:
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
        pos = chunk_search(chunk, type, depth)

        if pos != "NOT FOUND":
            return pos

    return pos


# ----------------------------------------

def chunk_search(chunk, type, depth):
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
                # result = False
                if part_unit_check(part, "", "", ""):
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
                if part_unit_check(part, "", "", ""):
                    return "N"

        # 과거분사구 (P)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbn", " ")
            elif result:
                result = False
                if part_unit_check(part, "", "", ""):
                    return "P"
        # 형용사절 (K)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ")
            elif result:
                result = False
                if part_unit_check(part, "", "", ""):
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
                    #return "I"
                    pattern = "I"
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
                    break

        return pattern


    return pattern




# ----------------------------------------

sum = 0


# for i in range(1, 13):  # 1 - 12 까지의 XML 불러오기
for i in range(0, 13):
    count = 0
    sum += Load_XML("/Users/deborah/Desktop/lango-django/lango_content/xml/" + str(i) + ".xml")  # Load_XML에 file Path를 인자로 전달 호출

print(sum)