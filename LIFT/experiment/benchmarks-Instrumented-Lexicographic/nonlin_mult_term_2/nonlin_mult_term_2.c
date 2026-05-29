#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (x <= 0)
        return 0;
    if (y <= 1)
        return 0;

    while (x < 10000)
    {
        printf("%d,%d\n", x, y);
        x = x * y;
    }
}
