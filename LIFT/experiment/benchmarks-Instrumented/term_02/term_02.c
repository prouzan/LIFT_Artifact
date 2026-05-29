#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x > y && y > z)
    {
        printf("x:%d,y:%d,z:%d\n", x, y, z);

        x = x - 3;
        y = y - 2;
        z = z - 1;
    }
}
