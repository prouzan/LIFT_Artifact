#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d", &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    y = 100;
    z = 1;
    while (x >= 0)
    {
        printf("x:%d,y:%d,z:%d\n", x, y, z);
        x = x - y;
        y = y - z;
        z = -z;
    }
    return 0;
}
