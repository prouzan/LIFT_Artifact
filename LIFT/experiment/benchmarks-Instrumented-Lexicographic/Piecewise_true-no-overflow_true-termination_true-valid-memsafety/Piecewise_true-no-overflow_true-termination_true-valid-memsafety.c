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
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (j > 0 && _i > 0 && _i != j)
    {
        printf("%d,%d\n", _i, j);

        if (j < _i)
        {
printf("L1\n");
            j = j - 1;
            _i = _nondet_int();
        }
        else if (_i < j)
        {
printf("L2\n");
            _i = _i - 1;
            j = _nondet_int();
        }
    }
    return 0;
}
