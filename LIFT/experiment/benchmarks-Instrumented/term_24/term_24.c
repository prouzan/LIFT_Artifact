#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    
    if (x > z || y > z)
        return 0;
    while (x != y)
    {
        printf("x:%d,y:%d,z:%d\n", x, y, z);

        x++;
        y++;
        if (x > z)
            x = z;
        if (y > z)
            y = y - 1;
    }
}
