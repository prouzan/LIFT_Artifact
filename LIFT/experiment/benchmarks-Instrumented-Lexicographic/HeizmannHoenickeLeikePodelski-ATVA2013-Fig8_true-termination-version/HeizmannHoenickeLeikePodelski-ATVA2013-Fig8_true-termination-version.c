#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (5 * y >= 1)
    {
        while (x >= 0)
        {
            printf("%d,%d\n", x, y);
            x = x - 4 * y + 3;
        }
    }
    return 0;
}
