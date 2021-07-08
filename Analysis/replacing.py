from konlpy.tag import Kkma
kma = Kkma()


def remove_double_plural(input_text):
    # 이중 복수 제거 함수

    plural_table = ((('수많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'NNG'), ('들', 'XSN')),
                    (('수많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'NNP'), ('들', 'XSN')),
                    (('수많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'UN'), ('들', 'XSN')),
                    (('많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'NNG'), ('들', 'XSN')),
                    (('많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'NNP'), ('들', 'XSN')),
                    (('많', 'VA'), ('은', 'ETD'), ('<_AL_>', 'UN'), ('들', 'XSN')),
                    (('여러', 'MDT'), ('<_AL_>', 'NNG'), ('들', 'XSN')),
                    (('여러', 'MDT'), ('<_AL_>', 'NNP'), ('들', 'XSN')),
                    (('여러', 'MDT'), ('<_AL_>', 'UN'), ('들', 'XSN')),
                    (('무리', 'NNG'), ('들', 'XSN'))
                    )

    result = ""
    pass_count = 0

    for line in input_text.split(". "):
        words = line.split(" ")

        for word_idx, word in enumerate(words):

            if pass_count > 0:
                pass_count -= 1
                continue

            morphs = (kma.pos(word))
            is_pattern_same = True
            used_word = 1

            for case in plural_table:
                for c, (rep, tag) in enumerate(case):
                    if len(morphs) <= c:
                        break

                    morph_check = rep != '<_AL_>' and rep != morphs[c][0]

                    if tag != morphs[c][1] and morph_check:
                        is_pattern_same = False
                        break

                    if len(morphs) <= c + 1 and len(words) > word_idx+1:
                        morphs.extend(kma.pos(words[word_idx+1]))
                        used_word += 1

                if is_pattern_same:
                    break

            if is_pattern_same:
                pass_count = used_word - 1

                for i in range(used_word-1):
                    result += words[word_idx + i]
                    result += ' '

                result += words[word_idx + used_word - 1][:words[word_idx + used_word - 1].rfind('들')] + words[word_idx + used_word - 1][words[word_idx + used_word - 1].rfind('들') + 1:]
                result += ' '
            else:
                result += word
                result += ' '

    return result


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
