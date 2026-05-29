#include <stdio.h>

int main() {
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    int _i, j, k;
    _i = 100;
    j = -1;
    k = 1;
    while (_i + j + k >= 1) {
        printf("_i:%d,j:%d,k:%d\n", _i, j, k);
        _i = _i - 1;
        j = j - 1;
        k = k + 1;
    }
    return 0;
}
