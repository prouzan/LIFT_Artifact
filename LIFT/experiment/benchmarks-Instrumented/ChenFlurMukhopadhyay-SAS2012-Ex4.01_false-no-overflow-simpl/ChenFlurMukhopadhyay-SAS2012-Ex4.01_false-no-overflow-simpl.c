#include <stdio.h>

int main()
{
    int x, y, n;
    scanf("%d%d%d", &x, &y, &n);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x + y >= 0 && x <= n)
    {
        printf("x:%d,y:%d,n:%d\n", x, y, n);
        x = 2 * x + y;
        y = y + 1;
    }
    return 0;
}
