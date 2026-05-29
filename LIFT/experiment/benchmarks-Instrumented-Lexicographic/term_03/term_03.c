#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x > y || y > z)
    {
        printf("%d,%d,%d\n", x, y, z);

        x = x - 3;
        y = y - 2;
        z = z - 1;
    }
}
