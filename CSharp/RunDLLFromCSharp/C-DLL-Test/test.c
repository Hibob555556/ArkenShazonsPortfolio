#include <stdio.h>

__declspec(dllexport) void printMsg(char *message);
void printMsg(char *message) {
    printf("%s\n", message);
}