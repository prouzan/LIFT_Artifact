#include <stdio.h>

int main()
{
    int c, _i, j, k, tmp;
    scanf("%d%d%d%d", &_i, &j, &k, &tmp);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    c = 0;

    while ((_i <= 100) && (j <= k) && (k > -2147483648))
    {
        printf("%d,%d,%d,%d\n", _i, j, k, tmp);

        tmp = _i;
        _i = j;
        j = tmp + 1;
        k = k - 1;
    }
    return 0;
}
