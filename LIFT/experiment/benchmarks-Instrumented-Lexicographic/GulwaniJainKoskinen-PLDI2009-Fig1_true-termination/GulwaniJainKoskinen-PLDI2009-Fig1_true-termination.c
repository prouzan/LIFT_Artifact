#include <stdio.h>

int main()
{
    int id, maxId, tmp;
    scanf("%d%d", &id, &maxId);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (0 <= id && id < maxId)
    {
        tmp = id + 1;
        while (tmp != id)
        {
            printf("%d,%d\n", id, maxId);
            if (tmp <= maxId)
            {
printf("L1\n");
                tmp = tmp + 1;
            }
            else
            {
printf("L2\n");
                tmp = 0;
            }
        }
    }

    return 0;
}
