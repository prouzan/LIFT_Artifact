#include<stdio.h>

int main()
{
    int x, y, oldx;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x >= 0 && y >= 0)
    {
        printf("x:%d,y:%d,oldx:%d\n", x, y, oldx);

		oldx = x;
		x = y - 1;
		y = oldx - 1;
    }
    return 0;
}
