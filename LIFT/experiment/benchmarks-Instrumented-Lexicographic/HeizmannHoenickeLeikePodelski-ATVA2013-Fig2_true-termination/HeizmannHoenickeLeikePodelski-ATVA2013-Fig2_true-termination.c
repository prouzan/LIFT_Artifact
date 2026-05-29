#include <stdio.h>

int main()
{
    int y;
    scanf("%d", &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    int x = y + 42;
    while (x >= 0)
    {
        printf("%d\n", y);
        y = 2 * y - x;
        x = (y + x) / 2;
    }
    return 0;
}
