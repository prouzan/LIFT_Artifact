#include <stdio.h>

int main()
{
    int a, b, q, olda;
    scanf("%d%d%d", &q, &a, &b);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (q > 0)
    {
        printf("%d,%d,%d\n", q, a, b);
        q = q + a - 1;
        olda = a;
        a = 3 * olda - 4 * b;
        b = 4 * olda + 3 * b;
    }
    return 0;
}
