#include <stdio.h>

int main()
{
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    int y = 2;
    while (x >= 0)
    {
        printf("%d\n", y);
        x = x - y;
        y = (y + 1) / 2;
    }
    return 0;
}
