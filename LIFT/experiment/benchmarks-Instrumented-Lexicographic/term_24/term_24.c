#include <stdio.h>

int main()
{
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    
    if (x > z || y > z)
        return 0;
    while (x != y)
    {
        printf("%d,%d,%d\n", x, y, z);

        x++;
        y++;
        if (x > z)
            {
printf("L1\n");x = z;}
        if (y > z)
            {
printf("L2\n");y = y - 1;}
    }
}
