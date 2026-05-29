#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (x > y)
    {
        while (x >= 0)
        {
            printf("%d,%d\n", x, y);
            y = 2 * y - x;
            x = (y + x + 1) / 2;
        }
    }
    return 0;
}
