#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (x <= y)
        return 0;

    while (x != y)
    {
        printf("%d,%d\n", x, y);

        x = x - 2;
        y = y - 1;
    }
}
