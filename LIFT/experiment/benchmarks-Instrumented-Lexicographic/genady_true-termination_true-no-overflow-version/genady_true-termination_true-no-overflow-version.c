#include <stdio.h>

int main() {
    int _i, j;
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    j = 1;
    _i = 10000;
    while (_i-j >= 1) {
        printf("#\n");
        j = j + 3;
        _i = _i - 2;
    }
    return 0;
}
