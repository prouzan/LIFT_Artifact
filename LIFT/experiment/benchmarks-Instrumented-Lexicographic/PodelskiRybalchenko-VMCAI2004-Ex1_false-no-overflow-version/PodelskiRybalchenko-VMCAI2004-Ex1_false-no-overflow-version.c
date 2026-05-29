#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void)
{
    return rand()%65535;
}

int main() {
    int _i, j, nondetNat, nondetPos, _i1, j1, nondetNat1, nondetPos1;
    scanf("%d%d%d%d", &_i, &j, &_i1, &j1);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (_i + _i1 - j - j1 >= 1) {
        printf("%d,%d,%d,%d\n", _i, j, _i1, j1);

        nondetNat = _nondet_int();
        if (nondetNat < 0) {
printf("L1\n");
            nondetNat = -nondetNat;
        }
        _i = _i - nondetNat;
        nondetPos = _nondet_int();
        if (nondetPos < 0) {
printf("L2\n");
            nondetPos = -nondetPos;
        }
        nondetPos = nondetPos + 1;
        j = j + nondetPos;


        nondetNat1 = _nondet_int();
        if (nondetNat1 < 0) {
printf("L3\n");
            nondetNat1 = -nondetNat1;
        }
        _i1 = _i1 - nondetNat1;
        nondetPos1 = _nondet_int();
        if (nondetPos1 < 0) {
printf("L4\n");
            nondetPos1 = -nondetPos1;
        }
        nondetPos1 = nondetPos1 + 1;
        j1 = j1 + nondetPos1;
    }
    return 0;
}
