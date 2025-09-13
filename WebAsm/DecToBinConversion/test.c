#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "main.h"

/*
 * Function: DecToBin
 * ------------------
 * Converts a decimal integer N to a binary string.
 * Also returns a padded binary string split into octets (8-bit groups) with spaces.
 *
 * Parameters:
 *   N              - Decimal integer to convert
 *   padded_binary  - Pointer to char* which will store the padded binary string with spaces
 *
 * Returns:
 *   char*          - Binary representation of N (without padding)
 */
char* DecToBin(int N, char** padded_binary)
{
    // Special case: if the number is 0
    if (N == 0) {
        *padded_binary = strdup("00000000"); // padded 8-bit representation
        return strdup("0");                  // binary representation
    }

    // Calculate number of bits needed to represent N
    int digits = (int)(log2(N)) + 1;

    // Allocate memory for binary string (without padding)
    char* bin_num = (char*)malloc(digits + 1);
    bin_num[digits] = '\0'; // null terminator

    // Fill the binary string from least significant bit to most significant
    int temp = N;
    for (int i = digits - 1; i >= 0; i--) {
        bin_num[i] = (temp % 2) + '0'; // convert remainder to '0' or '1'
        temp /= 2;                     // shift right
    }

    // Calculate how many leading zeros are needed to pad to full bytes
    int pad_size = (8 - (digits % 8)) % 8;
    int total_bits = digits + pad_size; // total bits after padding
    int octets = total_bits / 8;        // number of 8-bit groups

    // Allocate memory for padded binary string including spaces between octets
    int padded_len = total_bits + (octets - 1); // extra space for spaces
    char* padded_bin_num = (char*)malloc(padded_len + 1); // +1 for null terminator

    int bit_index = 0; // index in bin_num
    int j = 0;         // index in padded_bin_num

    // Build padded binary string with spaces
    for (int i = 0; i < total_bits; i++) {
        // Insert a space before each byte except the first
        if (i > 0 && i % 8 == 0) {
            padded_bin_num[j++] = ' ';
        }

        // Add leading zeros for padding
        if (i < pad_size) {
            padded_bin_num[j++] = '0';
        } else {
            padded_bin_num[j++] = bin_num[bit_index++]; // copy binary digits
        }
    }

    padded_bin_num[j] = '\0';         // null-terminate padded string
    *padded_binary = padded_bin_num;  // set the output pointer
    return bin_num;                   // return original binary string
}

int main() 
{
    int user_num;
    char* padded_binary;

    // Ask user for input
    printf("Enter Your Number: ");
    scanf("%d", &user_num);

    // Convert decimal to binary and get padded octet string
    char* binary_string = DecToBin(user_num, &padded_binary);

    // Print results
    printf("\n'%d' is '%s' in binary.", user_num, binary_string);
    printf("\nOctets: %s\n", padded_binary);

    // Free allocated memory to prevent leaks
    free(binary_string);
    free(padded_binary);
}
