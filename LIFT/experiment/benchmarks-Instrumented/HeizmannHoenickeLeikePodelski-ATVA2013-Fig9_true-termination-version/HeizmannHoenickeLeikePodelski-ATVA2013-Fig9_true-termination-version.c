#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (10 * y > z && z < 10)
    {
        while (x >= 0)
        {
            printf("x:%d,y:%d,z:%d\n", x, y, z);
            x = x - 10 * y + z;
        }
    }
    return 0;
}
