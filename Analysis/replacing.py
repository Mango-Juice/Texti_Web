from konlpy.tag import Kkma
kma = Kkma()


def remove_double_passive(input_text):
    # 이중피동 제거 함수
    replacing = ["이", "히", "리", "기"]
    words = input_text.split(" ")
    result = ""

    for word_idx, word in enumerate(words):
        changed_word = ""
        is_changed = False
        pass_count = 0
        tagged_morphs = kma.pos(word)

        for morph_idx, morph in enumerate(tagged_morphs):
            flag = True

            if pass_count > 0:
                pass_count -= 1
                continue

            if flag and morph[1] == "VV":
                if morph_idx < len(tagged_morphs) - 2 and tagged_morphs[morph_idx + 1][1] == "ECS" and tagged_morphs[morph_idx + 2][1] == "VXV":
                    for rep_idx, replaced in enumerate(["이어지", "히어지", "리어지", "기어지"]):
                        target = morph[0] + tagged_morphs[morph_idx+1][0] + tagged_morphs[morph_idx+2][0]
                        for idx in range(len(target)-2):
                            if replaced == target[idx:idx+3]:
                                changed_word += target[:idx] + replacing[rep_idx]
                                pass_count = 2
                                is_changed = True
                                flag = False
                else:
                    for rep_idx, replaced in enumerate(["여지", "혀지", "려지", "겨지"]):
                        target = morph[0]
                        for idx in range(len(target)-1):
                            if replaced == target[idx:idx+2]:
                                changed_word += target[:idx] + replacing[rep_idx]
                                is_changed = True
                                flag = False

                if flag:
                    changed_word += morph[0]

            else:
                changed_word += morph[0]

        if is_changed:
            result += " " + changed_word
        else:
            result += " " + word

    return result
