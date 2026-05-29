#include <stdio.h>

int main()
{
    int d, b;
    scanf("%d%d", &d, &b);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (d * b > 0)
    {
        printf("%d,%d\n", d, b);
        b = -b;
    }
}
