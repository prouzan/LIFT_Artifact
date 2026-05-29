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
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (_i + j + k >= 0)
    {
        printf("_i:%d,j:%d,k:%d\n", _i, j, k);
        if (_nondet_2() == 0)
            _i--;
        else
            j++;
        k = k - 2;
    }
    return 0;
}
