#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (10 * y > z && z < 10)
    {
        while (x >= 0)
        {
            printf("%d,%d,%d\n", x, y, z);
            x = x - 10 * y + z;
        }
    }
    return 0;
}
