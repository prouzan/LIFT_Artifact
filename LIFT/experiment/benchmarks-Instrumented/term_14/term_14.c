#include <stdio.h>
#include <stdlib.h>

int _nondet_2(void)
{
    return rand() % 2;
}

int main()
{
    int _i, j, a, b;
    scanf("%d%d%d%d", &_i, &j, &a, &b);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (_i + j + a + b == 0)
    {
        printf("_i:%d,j:%d,a:%d,b:%d\n", _i, j, a, b);
        if (_nondet_2() == 0)
            _i--;
        else
            j++;
        if (_nondet_2() == 0)
            a = a - 2;
        else
            b = b + 2; 
    }
    return 0;
}
