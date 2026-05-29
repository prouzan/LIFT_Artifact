#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d", &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    y = 100;
    z = 1;
    while (x >= 0)
    {
        printf("%d\n", x);
        x = x - y;
        y = y - z;
        z = -z;
    }
    return 0;
}
