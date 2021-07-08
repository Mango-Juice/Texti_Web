# coding=utf8
from konlpy.tag import Okt
okt = Okt()


def find_repeated(input_text):
    bound = int(len(input_text) / 250 + 3)
    preprocessed = okt.pos(input_text)
    repeat_count = {}
    treated = ('Adjective', 'Noun')

    for morph, tag in preprocessed:
        if tag not in treated:
            continue

        if morph in repeat_count:
            repeat_count[morph] += 1
        else:
            repeat_count[morph] = 1

    result = []

    for morph, count in repeat_count.items():
        if count > bound:
            result.append(morph)

    return result
