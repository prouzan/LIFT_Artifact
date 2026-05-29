#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x < 0 && y > 0)
    {
        printf("%d,%d\n", x, y);
        x = -3 * x - 17;
        y = -4 * y + 8;
    }
    return 0;
}
