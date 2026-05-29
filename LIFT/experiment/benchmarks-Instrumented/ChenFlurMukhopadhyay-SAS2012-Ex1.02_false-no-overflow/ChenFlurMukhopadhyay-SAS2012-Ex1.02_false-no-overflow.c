#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int _nondet_101(void){
    return rand()%101;
}

int main()
{
    srand(time(NULL));
    int x, oldx;
    scanf("%d", &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    oldx = _nondet_101();

    while (x > 0 && x < 100 && x >= 2 * oldx + 10)
    {
        printf("x:%d,oldx:%d\n", x, oldx);
        oldx = x;
        x = _nondet_101();
    }
    return 0;
}
