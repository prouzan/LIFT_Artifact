#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    int c1 = 0;
    int c2 = 0;

    while (x > y)
    {
        printf("%d,%d\n", x, y);
        x = x + c1 / 3;
        y = y + c2 / 2;
        c1 = c1 + 2;
        c2 = c2 + 3;
    }
}
