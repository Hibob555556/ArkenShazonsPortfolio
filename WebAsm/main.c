// main.c
#include <stdio.h>
#include <stdlib.h>
#include <emscripten.h>

// add 2 numbers
EMSCRIPTEN_KEEPALIVE
int add(int a, int b) 
{
    return a + b;
}

// multiply 2 numbers
EMSCRIPTEN_KEEPALIVE
int mult(int a, int b) 
{
    return a * b;
}

// generate n numbers of the fibonacci sequence up to 46
EMSCRIPTEN_KEEPALIVE
int* fib(int count) 
{
    // create array
    int* fibNums = (int*)malloc(count * sizeof(int));

    // ensure it is valid
    if (!fibNums) return NULL;

    // iterate until we reach the desired number
    for (int i = 0; i < count; i++) {
        if (i == 0) {
            fibNums[i] = 0;  // or 1 if you prefer starting at 1
        } else if (i == 1) {
            fibNums[i] = 1;
        } else {
            fibNums[i] = fibNums[i - 1] + fibNums[i - 2];
        }
    }

    // return our array
    return fibNums;
}