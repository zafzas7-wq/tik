"""Seminar 8: Hamming code (even parity), one-bit error correction."""


def check_bits(bits):
    if not bits or any(bit not in '01' for bit in bits):
        raise ValueError('Only a non-empty binary string (0 and 1) is allowed.')


def control_count(data_length):
    if data_length <= 0:
        raise ValueError('Data length must be positive.')
    r = 0
    while (1 << r) < data_length + r + 1:
        r += 1
    return r


def encode(data):
    """Return a Hamming code. Positions are numbered 1..n from the LEFT."""
    check_bits(data)
    r = control_count(len(data))
    n = len(data) + r
    result = ['0'] * (n + 1)
    iterator = iter(data)
    for position in range(1, n + 1):
        if position & (position - 1):  # not a power of 2: data position
            result[position] = next(iterator)
    for bit in range(r):
        parity_position = 1 << bit
        parity = 0
        for position in range(1, n + 1):
            if position & parity_position:
                parity ^= int(result[position])
        result[parity_position] = str(parity)
    return ''.join(result[1:])


def decode(received):
    """Return (syndrome, corrected_code, original_data).

    This basic Hamming code assumes at most ONE flipped bit.
    It cannot reliably identify two-bit errors.
    """
    check_bits(received)
    n = len(received)
    r = 0
    while (1 << r) <= n:
        r += 1
    syndrome = 0
    for bit in range(r):
        mask = 1 << bit
        parity = 0
        for position in range(1, n + 1):
            if position & mask:
                parity ^= int(received[position - 1])
        if parity:
            syndrome += mask
    if syndrome > n:
        raise ValueError('Invalid syndrome for code length: multiple errors or invalid input.')
    corrected = list(received)
    if syndrome:
        index = syndrome - 1
        corrected[index] = '1' if corrected[index] == '0' else '0'
    corrected_code = ''.join(corrected)
    data = ''.join(bit for position, bit in enumerate(corrected_code, 1)
                   if position & (position - 1))
    return syndrome, corrected_code, data


def hamming_distance(first, second):
    check_bits(first)
    check_bits(second)
    if len(first) != len(second):
        raise ValueError('Strings must have the same length.')
    return sum(a != b for a, b in zip(first, second))


if __name__ == '__main__':
    data = '11001001'  # Seminar 8, example 3
    code = encode(data)
    print('Seminar 8 — Hamming code')
    print('Original data:', data)
    print('Encoded code:', code)
    corrupted = code[:2] + ('1' if code[2] == '0' else '0') + code[3:]
    print('Received with one error:', corrupted)
    position, fixed, decoded_data = decode(corrupted)
    print('Error position (from left):', position)
    print('Corrected code:', fixed)
    print('Recovered data:', decoded_data)
    print('Distance (100101100, 110110101):', hamming_distance('100101100', '110110101'))
