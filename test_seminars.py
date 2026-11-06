import unittest
from seminar8_hamming import encode, decode, hamming_distance
from seminar9_fano import (is_prefix_free, is_postfix_free, encode_message,
                           decode_prefix, decode_postfix, average_length, min_fixed_length)


class SeminarTests(unittest.TestCase):
    def test_hamming_examples(self):
        self.assertEqual(encode('0101'), '0100101')
        self.assertEqual(encode('11001001'), '111010001001')
        self.assertEqual(decode('110010001001'), (3, '111010001001', '11001001'))

    def test_hamming_all_single_bit_positions(self):
        data = '10011010'
        code = encode(data)
        for i in range(len(code)):
            damaged = code[:i] + str(1 - int(code[i])) + code[i + 1:]
            self.assertEqual(decode(damaged), (i + 1, code, data))

    def test_hamming_distance(self):
        self.assertEqual(hamming_distance('100101100', '110110101'), 4)

    def test_prefix_codes(self):
        codes = {'A': '0', 'B': '10', 'C': '110', 'D': '111'}
        self.assertTrue(is_prefix_free(codes))
        self.assertEqual(decode_prefix('0110110111', codes), 'ACCD')
        self.assertEqual(decode_prefix(encode_message('ABCD', codes), codes), 'ABCD')

    def test_postfix_codes(self):
        codes = {'A': '0', 'B': '01', 'C': '011', 'D': '111'}
        self.assertTrue(is_postfix_free(codes))
        self.assertFalse(is_prefix_free(codes))
        self.assertEqual(decode_postfix(encode_message('ABCD', codes), codes), 'ABCD')

    def test_efficiency(self):
        a = {'A': '0', 'B': '10', 'C': '110', 'D': '111'}
        b = {'A': '00', 'B': '01', 'C': '10', 'D': '11'}
        f = {'A': 50, 'B': 25, 'C': 15, 'D': 10}
        self.assertAlmostEqual(average_length(a, f), 1.75)
        self.assertAlmostEqual(average_length(b, f), 2)
        self.assertEqual(min_fixed_length(23), 5)


if __name__ == '__main__':
    unittest.main()
