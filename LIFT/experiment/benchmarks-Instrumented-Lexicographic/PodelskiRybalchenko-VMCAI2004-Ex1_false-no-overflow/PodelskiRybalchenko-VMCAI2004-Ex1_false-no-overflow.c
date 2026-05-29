#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void)
{
    return rand()%65535;
}

int main() {
    int _i, j, nondetNat, nondetPos;
    scanf("%d%d", &_i, &j);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (_i - j >= 1) {
        printf("%d,%d\n", _i, j);

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
    }
    return 0;
}
