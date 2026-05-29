#include <stdio.h>

int main()
{
    int x, y;
    x = 1;
    scanf("%d", &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (y <= 1)
        return 0;

    while (x < 10000)
    {
        printf("x:%d,y:%d\n", x, y);
        x = x * y;
    }
}
