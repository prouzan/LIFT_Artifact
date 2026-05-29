#include <stdio.h>

int main()
{
    int x, y;
    x = 1;
    scanf("%d", &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (y <= 1)
        return 0;

    while (x < 10000)
    {
        printf("%d\n", y);
        x = x * y;
    }
}
