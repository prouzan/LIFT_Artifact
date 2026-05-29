#include <stdio.h>

int main() {
    int _i, j;
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    j = 1;
    _i = 10000;
    while (_i-j >= 1) {
        printf("_i:%d,j:%d\n", _i, j);
        j = j + 3;
        _i = _i - 2;
    }
    return 0;
}
