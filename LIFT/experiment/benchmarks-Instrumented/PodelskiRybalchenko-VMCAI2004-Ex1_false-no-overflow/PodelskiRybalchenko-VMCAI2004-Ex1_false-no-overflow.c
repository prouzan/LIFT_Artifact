#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void)
{
    return rand()%65535;
}

int main() {
    int _i, j, nondetNat, nondetPos;
    scanf("%d%d", &_i, &j);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (_i - j >= 1) {
        printf("_i:%d,j:%d,nondetNat:%d,nondetPos:%d\n", _i, j, nondetNat, nondetPos);

        nondetNat = _nondet_int();
        if (nondetNat < 0) {
            nondetNat = -nondetNat;
        }
        _i = _i - nondetNat;
        nondetPos = _nondet_int();
        if (nondetPos < 0) {
            nondetPos = -nondetPos;
        }
        nondetPos = nondetPos + 1;
        j = j + nondetPos;
    }
    return 0;
}
