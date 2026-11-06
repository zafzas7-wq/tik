"""Seminar 9: Prefix/postfix codes, Fano conditions, and code efficiency."""
from math import ceil, log2


def valid_codes(codes):
    if not codes or not all(isinstance(word, str) and word and set(word) <= {'0', '1'} for word in codes.values()):
        raise ValueError('All codes must be non-empty binary strings.')
    if len(set(codes.values())) != len(codes):
        raise ValueError('Code words must be distinct.')


def is_prefix_free(codes):
    valid_codes(codes)
    words = list(codes.values())
    return all(not b.startswith(a) for i, a in enumerate(words)
               for j, b in enumerate(words) if i != j)


def is_postfix_free(codes):
    valid_codes(codes)
    words = list(codes.values())
    return all(not b.endswith(a) for i, a in enumerate(words)
               for j, b in enumerate(words) if i != j)


def encode_message(message, codes):
    valid_codes(codes)
    return ''.join(codes[symbol] for symbol in message)


def decode_prefix(bits, codes):
    valid_codes(codes)
    if not is_prefix_free(codes):
        raise ValueError('Fano prefix condition is not met.')
    if any(bit not in '01' for bit in bits):
        raise ValueError('The message must be binary.')
    reverse = {code: symbol for symbol, code in codes.items()}
    result, current = [], ''
    for bit in bits:
        current += bit
        if current in reverse:
            result.append(reverse[current])
            current = ''
    if current:
        raise ValueError('The message ends with an incomplete code word.')
    return ''.join(result)


def decode_postfix(bits, codes):
    valid_codes(codes)
    if not is_postfix_free(codes):
        raise ValueError('Reverse Fano condition is not met.')
    if any(bit not in '01' for bit in bits):
        raise ValueError('The message must be binary.')
    reverse = {code: symbol for symbol, code in codes.items()}
    result, current = [], ''
    for bit in reversed(bits):
        current = bit + current
        if current in reverse:
            result.append(reverse[current])
            current = ''
    if current:
        raise ValueError('The message starts with an incomplete code word.')
    return ''.join(reversed(result))


def average_length(codes, frequencies):
    valid_codes(codes)
    if set(codes) != set(frequencies) or any(v < 0 for v in frequencies.values()):
        raise ValueError('Each symbol must have a nonnegative frequency.')
    total = sum(frequencies.values())
    if total <= 0:
        raise ValueError('Frequencies must sum to a positive value.')
    return sum((freq / total) * len(codes[symbol])
               for symbol, freq in frequencies.items())


def min_fixed_length(alphabet_size):
    if alphabet_size <= 0:
        raise ValueError('Alphabet size must be positive.')
    return (alphabet_size - 1).bit_length()


if __name__ == '__main__':
    code_a = {'A': '0', 'B': '10', 'C': '110', 'D': '111'}
    code_b = {'A': '00', 'B': '01', 'C': '10', 'D': '11'}
    frequencies = {'A': 50, 'B': 25, 'C': 15, 'D': 10}
    message = 'ABCD'
    encoded = encode_message(message, code_a)
    print('Seminar 9 — Fano condition')
    print('Prefix-free:', is_prefix_free(code_a))
    print('Postfix-free:', is_postfix_free(code_a))
    print('Message:', message, '->', encoded, '->', decode_prefix(encoded, code_a))
    print('Code A average length:', average_length(code_a, frequencies))
    print('Code B average length:', average_length(code_b, frequencies))
    print('Minimum fixed-length bits for 23 symbols:', min_fixed_length(23))
