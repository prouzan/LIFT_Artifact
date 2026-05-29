#include <stdio.h>
#include <stdlib.h>

int _nondet_2(void){
    return rand()%2;
}

int main()
{
    int x, y, N;
    scanf("%d%d%d", &x, &y, &N);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (N < 536870912 && x < 536870912 && y < 536870912 && x >= -1073741824)
    {
        if (x + y >= 0)
        {
            while (x <= N)
            {
                printf("%d,%d,%d\n", x, y, N);
                if (_nondet_2() != 0)
                {
printf("L1\n");
                    x = 2 * x + y;
                    y = y + 1;
                }
                else
                {
printf("L2\n");
                    x = x + 1;
                }
            }
        }
    }
    return 0;
}
