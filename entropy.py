from argparse import ArgumentParser
from collections import Counter, namedtuple
from math import log2
from typing import List

UKR_ALPHABET_SET = set('абвгґдеєжзиіїйклмнопрстуфхцчшщьюя')
B64_ALPHABET_SET = set(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
)

assert len(UKR_ALPHABET_SET) == 33

CharFreq = namedtuple('CharFreq', ['char', 'frequency'])


def calc_avg_entropy(char_frequencies: List[CharFreq]) -> float:
    return -sum(x.frequency * log2(x.frequency) for x in char_frequencies)


def calc_text_info_amount(avg_entropy: float, total_words: int) -> float:
    return avg_entropy * total_words


def normalize_text(text: str, alphabet_set: set) -> str:
    lower = [symbol.lower() for symbol in text]
    return ''.join(symbol for symbol in lower if symbol in alphabet_set)


def calc_word_frequencies(normalized_words: str) -> List[CharFreq]:
    word_stats = Counter(normalized_words)
    return [
        CharFreq(char=word, frequency=word_stats[word] / len(normalized_words))
        for word in word_stats
    ]


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def fmt_float(val):
    return '%.3f' % val


def parse_cmd_args():
    parser = ArgumentParser()
    parser.add_argument('file', type=str, help='path to the file')
    parser.add_argument('-b64', action='store_true')
    return parser.parse_args()


def main():
    args = parse_cmd_args()
    with open(args.file) as file:
        txt_content = file.read()

    alphabet = UKR_ALPHABET_SET if not args.b64 else B64_ALPHABET_SET

    normalized = normalize_text(txt_content, alphabet)
    word_frequencies = calc_word_frequencies(normalized)
    avg_entropy = calc_avg_entropy(word_frequencies)
    text_info_amount = calc_text_info_amount(avg_entropy, len(normalized))

    print('_' * 10 + 'STATS' + '_' * 10)
    print(f'AVERAGE TEXT ENTROPY: {fmt_float(avg_entropy)}')
    print(f'AMOUNT OF INFO: {fmt_float(text_info_amount)}')
    parts_of_3 = list(chunks(
        [f'{x.char}: {fmt_float(x.frequency)}'
         for x in sorted(word_frequencies, key=lambda w: w.char)], 3
    ))
    words_table = '\n'.join(
        '  '.join(part) for part in parts_of_3
    )
    print(f'WORD FREQUENCIES:\n{words_table}')


if __name__ == '__main__':
    main()
