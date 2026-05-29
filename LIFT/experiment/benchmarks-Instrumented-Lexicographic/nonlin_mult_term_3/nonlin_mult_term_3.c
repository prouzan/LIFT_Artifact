#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (x <= 0)
        return 0;
    if (y <= 1)
        return 0;
    if (z <= 1)
        return 0;

    while (x < 1000000)
    {
        printf("%d,%d,%d\n", x, y, z);
        x = x * y * z;
    }
}
