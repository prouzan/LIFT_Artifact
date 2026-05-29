#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void)
{
    return rand();
}

int main()
{
    int y, z;
    scanf("%d%d", &y, &z);

    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    if (!(-1073741823 <= y && y <= 1073741823))
        return 0;
    if (!(z <= 1073741823))
        return 0;
    while (z >= 0)
    {
        printf("%d,%d\n", y, z);

        y = y - 1;
        if (y >= 0)
        {
printf("L1\n");
            z = _nondet_int();
            //prevent overflow
            if (!(z <= 1073741823))
                return 0;
        }
        else
        {
printf("L2\n");
            z = z - 1;
        }
    }
    return 0;
}
