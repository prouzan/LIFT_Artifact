#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x - y > 0)
    {
        printf("%d,%d\n", x, y);
        x = y - x;
        y = y + 1;
    }
    return 0;
}
