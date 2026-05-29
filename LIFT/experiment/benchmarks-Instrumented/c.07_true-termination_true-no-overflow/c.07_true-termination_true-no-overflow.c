#include <stdio.h>

int main()
{
    int c, _i, j, k, tmp;
    scanf("%d%d%d%d", &_i, &j, &k, &tmp);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    c = 0;

    while ((_i <= 100) && (j <= k) && (k > -2147483648))
    {
        printf("c:%d,_i:%d,j:%d,k:%d,tmp:%d\n", c, _i, j, k, tmp);

        tmp = _i;
        _i = j;
        j = tmp + 1;
        k = k - 1;
    }
    return 0;
}
