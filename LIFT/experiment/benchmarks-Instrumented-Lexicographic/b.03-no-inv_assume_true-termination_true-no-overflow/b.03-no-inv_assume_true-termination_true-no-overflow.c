#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (x > 0)
    {
        while (x > y && y <= 2147483647 - x)
        {
            printf("%d,%d\n", x,y);
            y = y + x;
        }
    }
    return 0;
}
