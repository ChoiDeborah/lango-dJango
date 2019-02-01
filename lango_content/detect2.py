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
    #if (result != "NO PATTERN"):
        #print(result + "\n" + string + "\n\n")

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

    head = get_type(node)
    pattern = ""

    if head != "":
        print(head)

    if head == "BE":
        count = 0
        for part in node.findall("part"):
            if(count == 1):         #be + pattern(패턴)
                pattern = part_search(part, 0)
            count += 1
        if pattern == "nn":   # 명사구
            print("-CN10")
            type ="BE-CN10"
        elif pattern == "M":  # 동명사구
            print("-CN20")
            type = "BE-CN20"
        elif pattern == "G":  # to부정사구
            print("-CN30")
            type = "BE-CN30"
        elif pattern == "J":  # 명사절
            print("-CN40")
            type = "BE-CN40"
        elif pattern == "T":  # 원형부정사
            print("-CN50")
            type = "BE-CN50"
        elif pattern == "aj": # 형용사구
            print("-CJ10")
            type = "BE-CJ10"
        elif pattern == "R":  # 전치사
            print("-CJ20")
            type = "BE-CJ20"
        elif pattern == "N":  # 현재분사구
            print("-CJ30")
            type = "BE-CJ30"
        elif pattern == "P":  # 과거분사구
            print("-CJ40")
            type = "BE-CJ40"







    if head == "SV":
        count = 0
        for part in node.findall("part"):
            if (count == 1):  # be + pattern(패턴)
                pattern = part_search(part, 0)
            count += 1
        if pattern == "nn":   # 명사구
            print("-CN10")
            type ="SV-CN10"
        elif pattern == "M":  # 동명사구
            print("-CN20")
            type = "SV-CN20"
        elif pattern == "G":  # to부정사구
            print("-CN30")
            type = "SV-CN30"
        elif pattern == "J":  # 명사절
            print("-CN40")
            type = "SV-CN40"
        elif pattern == "T":  # 원형부정사
            print("-CN50")
            type = "SV-CN50"
        elif pattern == "aj": # 형용사구
            print("-CJ10")
            type = "SV-CJ10"
        elif pattern == "R":  # 전치사
            print("-CJ20")
            type = "SV-CJ20"
        elif pattern == "N":  # 현재분사구
            print("-CJ30")
            type = "SV-CJ30"
        elif pattern == "P":  # 과거분사구
            print("-CJ40")
            type = "SV-CJ40"

    #if head == "VB":


    #return type


# ----------------------------------------
def get_type(node):

    count = 0
    type = ""

    # be동사
    for part in node.findall("part"):
        if part_unit_check(part, "prd|trg", "", " lemma:be ", 0):
            type = "BE"

    # 상태동사
    for part in node.findall("part"):
        if part_unit_check(part, "prd|trg", "", " !lemma:be ", 0):
            type = "SV"

    # 일반동사
    for part in node.findall("part"):
        if count == 1:
            if part_unit_check(part, "obj", "", " ", 0):
                type = "VB"
        count += 1

    return type

def part_unit_check(part, role, pos, text, depth):

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
    xml_part_role = part.get("role")
    wordText = False

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
    chunkText = False

    word_pos = ""
    chunk_pos = ""

    # word 존재 시
    for word in part.findall("word"):
        wordText = True
        word_pos = word.get("pos")
        #return pos

    # chunk 존재 시
    for chunk in part.findall("chunk"):
        chunkText = True
        chunk_pos = chunk_search(chunk, depth)
        #return pos

    if wordText and chunkText:
        chunk_pos = chunk_search(chunk, depth)
        return chunk_pos

    if wordText and not chunkText:
        return word_pos

    if not wordText and chunkText:
        return chunk_pos

    if not wordText and not chunkText:
        pos = "NOT FOUND"

    return pos


# ----------------------------------------

def chunk_search(chunk, depth):
    pattern = "NOT FOUND"

    chunk_pos = chunk.get("pos")

    result = False

    if chunk_pos == 'nn':
        # to부정사구 (G)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "", " to ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "prd", "", "", depth):
                    return "G"
        # 동명사구 (M)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "prd", "", "", depth):
                    return "M"

        # 명사절 (J)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ", depth+1)
            elif result:
                # result = False
                if part_unit_check(part, "", "", "", depth):
                    return "J"

        # 원형부정사 (T)
        for part in chunk.findall("part"):
            if part_unit_check(part, "prd", "", "", depth):
                return "T"

    if chunk_pos == 'aj':
        # 전치사구 (R)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "pp", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "obj", "", "", depth):
                    return "R"

        # 현재분사구 (N)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "", "", "", depth):
                    return "N"

        # 과거분사구 (P)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbn", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "", "", "", depth):
                    return "P"
        # 형용사절 (K)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "", "", "", depth):
                    return "K"

        # to부정사구 (H)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "", " to ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "prd", "", "", depth):
                    return "H"

    # 부사
    if chunk_pos == 'av':

        # to부정사구 (I)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "", " to ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "prd", "", "", depth):
                    return "I"

        # 부사절(L)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "cj", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "", "", "", depth+1):
                    return "L"

        # 현재분사구 (O)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbg", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "", "", "", depth):
                    return "O"

        # 과거분사구 (Q)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "vbn", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "", "", "", depth):
                    return "Q"

            # 전치사구 (S)
        for part in chunk.findall("part"):
            if not result:
                result = part_unit_check(part, "trg", "pp", " ", depth+1)
            elif result:
                result = False
                if part_unit_check(part, "obj", "", "", depth):
                    return "S"

    return pattern




# ----------------------------------------

sum = 0


# for i in range(1, 13):  # 1 - 12 까지의 XML 불러오기
for i in range(1, 13):
    count = 0
    sum += Load_XML("/Users/deborah/Desktop/lango-django/lango_content/xml/" + str(i) + ".xml")  # Load_XML에 file Path를 인자로 전달 호출

print(sum)