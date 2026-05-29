#include <stdio.h>

int main()
{
    int _i = 1;
    int j = 1;
    int d, b;
    scanf("%d%d", &d, &b);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (b <= 1)
        return 0;
    if (b <= d)
        return 0;

    while (_i >= j)
    {
        printf("%d,%d\n", d, b);

        _i = _i * d;
        j = j * b;
    }
}
