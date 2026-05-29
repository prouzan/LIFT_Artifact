#include <stdio.h>

int main()
{
    int x, y, n;
    scanf("%d%d%d", &x, &y, &n);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x + y >= 0 && x <= n)
    {
        printf("%d,%d,%d\n", x, y, n);
        x = 2 * x + y;
        y = y + 1;
    }
    return 0;
}
