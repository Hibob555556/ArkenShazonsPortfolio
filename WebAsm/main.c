// main.c
#include <stdio.h>
#include <stdlib.h>
#include <emscripten.h>

EMSCRIPTEN_KEEPALIVE
int add(int a, int b) 
{
    return a + b;
}

EMSCRIPTEN_KEEPALIVE
int mult(int a, int b) 
{
    return a * b;
}

EMSCRIPTEN_KEEPALIVE
int* fib(int count) 
{
    int* fibNums = (int*)malloc(count * sizeof(int));
    if (!fibNums) return NULL;

    for (int i = 0; i < count; i++) {
        if (i == 0) {
            fibNums[i] = 0;  // or 1 if you prefer starting at 1
        } else if (i == 1) {
            fibNums[i] = 1;
        } else {
            fibNums[i] = fibNums[i - 1] + fibNums[i - 2];
        }
    }
    return fibNums;
}