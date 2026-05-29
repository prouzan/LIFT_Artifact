#include <stdio.h>

int main() {
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    int _i, j, k;
    _i = 100;
    j = -1;
    k = 1;
    while (_i + j + k >= 1) {
        printf("#\n");
        _i = _i - 1;
        j = j - 1;
        k = k + 1;
    }
    return 0;
}
