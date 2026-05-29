#include <stdio.h>

int main()
{
    int x, y, r;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    r = 1;
    while (y > 0)
    {
        printf("%d,%d\n", x, y);
        r = r * x;
        y = y - 1;
    }
    return 0;
}
