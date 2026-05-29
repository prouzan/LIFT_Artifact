#include<stdio.h>

int main()
{
    int x, y, z, oldx;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x >= 0 || y >= 0 || z >= 0)
    {
        printf("x:%d,y:%d,z:%d,oldx:%d\n", x, y, z, oldx);

        oldx = x;
        x = y - 1;
        y = z - 1;
        z = oldx - 1;
    }
    return 0;
}
