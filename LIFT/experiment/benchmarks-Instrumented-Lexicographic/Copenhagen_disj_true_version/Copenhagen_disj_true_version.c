#include<stdio.h>

int main()
{
    int x, y, z, oldx;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x >= 0 || y >= 0 || z >= 0)
    {
        printf("%d,%d,%d\n", x, y, z);

        oldx = x;
        x = y - 1;
        y = z - 1;
        z = oldx - 1;
    }
    return 0;
}
