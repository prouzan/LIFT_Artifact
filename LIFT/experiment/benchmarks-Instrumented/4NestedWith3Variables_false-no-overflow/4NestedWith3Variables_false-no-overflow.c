#include <stdio.h>

int main()
{
    int a, b, q, olda;
    scanf("%d%d%d", &q, &a, &b);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (q > 0)
    {
        printf("a:%d,b:%d,q:%d,olda:%d\n", a, b, q, olda);
        q = q + a - 1;
        olda = a;
        a = 3 * olda - 4 * b;
        b = 4 * olda + 3 * b;
    }
    return 0;
}
