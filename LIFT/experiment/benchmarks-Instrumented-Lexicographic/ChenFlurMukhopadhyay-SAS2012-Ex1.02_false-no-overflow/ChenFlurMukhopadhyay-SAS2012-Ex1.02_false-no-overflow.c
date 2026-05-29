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
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    oldx = _nondet_101();

    while (x > 0 && x < 100 && x >= 2 * oldx + 10)
    {
        printf("%d\n", x);
        oldx = x;
        x = _nondet_101();
    }
    return 0;
}
