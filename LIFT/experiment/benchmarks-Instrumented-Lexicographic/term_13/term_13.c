#include <stdio.h>
#include <stdlib.h>

int _nondet_2(void)
{
    return rand() % 2;
}

int main()
{
    int _i, j, k;
    scanf("%d%d%d", &_i, &j, &k);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (_i + j + k >= 0)
    {
        printf("%d,%d,%d\n", _i, j, k);
        if (_nondet_2() == 0)
            {
printf("L1\n");_i--;}
        else
            {
printf("L2\n");j++;}
        k = k - 2;
    }
    return 0;
}
