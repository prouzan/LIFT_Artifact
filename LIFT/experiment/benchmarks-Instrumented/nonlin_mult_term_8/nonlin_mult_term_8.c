#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (x <= 1)
        return 0;
    if (y <= 1)
        return 0;
    if (z <= 1)
        return 0;
    while (x < 1000000)
    {
        printf("x:%d,y:%d,z:%d\n", x, y, z);
        x = x * y;
        y = y * z;
    }
}
