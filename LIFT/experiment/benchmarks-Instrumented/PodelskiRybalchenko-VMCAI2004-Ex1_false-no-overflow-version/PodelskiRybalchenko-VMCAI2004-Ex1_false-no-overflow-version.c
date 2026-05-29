#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void)
{
    return rand()%65535;
}

int main() {
    int _i, j, nondetNat, nondetPos, _i1, j1, nondetNat1, nondetPos1;
    scanf("%d%d%d%d", &_i, &j, &_i1, &j1);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (_i + _i1 - j - j1 >= 1) {
        printf("_i:%d,j:%d,nondetNat:%d,nondetPos:%d,_i1:%d,j1:%d,nondetNat1:%d,nondetPos1:%d\n", _i, j, nondetNat, nondetPos, _i1, j1, nondetNat1, nondetPos1);

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


        nondetNat1 = _nondet_int();
        if (nondetNat1 < 0) {
            nondetNat1 = -nondetNat1;
        }
        _i1 = _i1 - nondetNat1;
        nondetPos1 = _nondet_int();
        if (nondetPos1 < 0) {
            nondetPos1 = -nondetPos1;
        }
        nondetPos1 = nondetPos1 + 1;
        j1 = j1 + nondetPos1;
    }
    return 0;
}
