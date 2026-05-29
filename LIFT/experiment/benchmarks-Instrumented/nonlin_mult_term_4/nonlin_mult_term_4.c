#include <stdio.h>

int main()
{
    int _i = 1;
    int j = 1;
    int d, b;
    scanf("%d%d", &d, &b);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (b <= 1)
        return 0;
    if (b <= d)
        return 0;

    while (_i >= j)
    {
        printf("_i:%d,j:%d,d:%d,b:%d\n", _i, j, d, b);

        _i = _i * d;
        j = j * b;
    }
}
