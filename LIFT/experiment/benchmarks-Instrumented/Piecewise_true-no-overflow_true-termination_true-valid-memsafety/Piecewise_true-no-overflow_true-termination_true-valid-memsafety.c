#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void)
{
    return rand();
}

int main()
{
    int _i, j;
    scanf("%d%d", &_i, &j);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (j > 0 && _i > 0 && _i != j)
    {
        printf("_i:%d,j:%d\n", _i, j);

        if (j < _i)
        {
            j = j - 1;
            _i = _nondet_int();
        }
        else if (_i < j)
        {
            _i = _i - 1;
            j = _nondet_int();
        }
    }
    return 0;
}
