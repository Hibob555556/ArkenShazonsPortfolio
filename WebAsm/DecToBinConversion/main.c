#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <emscripten.h>

/*
 * Function: DecToBin
 * ------------------
 * Converts a decimal integer N to a binary string.
 * Returns a padded binary string split into octets (8-bit groups) with spaces.
 *
 * Parameters:
 *   N - Decimal integer to convert
 *
 * Returns:
 *   char* - Binary representation (malloc'ed, caller responsible for freeing)
 */
EMSCRIPTEN_KEEPALIVE
char* DecToBin(int N)
{
    if (N == 0) {
        return strdup("00000000");
    }

    int digits = (int)(log2(N)) + 1;

    char* bin_num = (char*)malloc(digits + 1);
    bin_num[digits] = '\0';

    int temp = N;
    for (int i = digits - 1; i >= 0; i--) {
        bin_num[i] = (temp % 2) + '0';
        temp /= 2;
    }

    int pad_size = (8 - (digits % 8)) % 8;
    int total_bits = digits + pad_size;
    int octets = total_bits / 8;

    int padded_len = total_bits + (octets - 1);
    char* padded_bin_num = (char*)malloc(padded_len + 1);

    int bit_index = 0;
    int j = 0;

    for (int i = 0; i < total_bits; i++) {
        if (i > 0 && i % 8 == 0) {
            padded_bin_num[j++] = ' ';
        }

        if (i < pad_size) {
            padded_bin_num[j++] = '0';
        } else {
            padded_bin_num[j++] = bin_num[bit_index++];
        }
    }

    padded_bin_num[j] = '\0';
    free(bin_num);

    return padded_bin_num;
}

/*
 * Function: BinToDec
 * ------------------
 * Converts a binary string (e.g., "1011") to a decimal integer.
 *
 * Parameters:
 *   binStr - Null-terminated binary string
 *
 * Returns:
 *   int - Decimal value
 */
EMSCRIPTEN_KEEPALIVE
int BinToDec(const char* binStr)
{
    int decimal = 0;
    while (*binStr)
    {
        if (*binStr == '0' || *binStr == '1') {
            decimal = decimal * 2 + (*binStr - '0');
        }
        binStr++;
    }
    return decimal;
}
