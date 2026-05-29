#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (x <= 0)
        return 0;
    if (y <= 1)
        return 0;

    while (x < 10000)
    {
        printf("x:%d,y:%d,z:%d\n", x, y, z);
        x = x * y;
    }
}
