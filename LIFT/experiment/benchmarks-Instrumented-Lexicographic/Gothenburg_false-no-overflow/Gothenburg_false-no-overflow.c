#include <stdio.h>

int main()
{
    int a, b, x, y;
    scanf("%d%d%d%d", &a, &b, &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (a == b)
    {
        while (x >= 0 || y >= 0)
        {
            printf("%d,%d,%d,%d\n", a, b, x, y);

            x = x + a - b - 1;
            y = y + b - a - 1;
        }
    }
    return 0;
}
