#include <stdio.h>

int main()
{
    int j, b;
    scanf("%d%d", &j, &b);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (b <= 1)
        return 0;

    while (j < 100)
    {
        printf("j:%d,b:%d\n", j, b);
        if (j <= 0)
            j = 1;
        else
            j = j * b;
    }
}
