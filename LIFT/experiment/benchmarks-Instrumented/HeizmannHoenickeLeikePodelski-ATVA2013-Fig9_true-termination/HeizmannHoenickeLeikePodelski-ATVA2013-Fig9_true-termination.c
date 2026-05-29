#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (2 * y >= z)
    {
        while (x >= 0 && z == 1)
        {
            printf("x:%d,y:%d,z:%d\n", x, y, z);
            x = x - 2 * y + 1;
        }
    }
    return 0;
}
