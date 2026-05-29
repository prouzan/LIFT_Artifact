#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (x >= 0) {
        printf("%d,%d,%d\n", x, y, z);
        if (_nondet_2() != 0) {
printf("L1\n");
            x = x + y;
        } else {
printf("L2\n");
            x = x + z;
        }
        y = y + z;
        z = z - 1;
    }
    return 0;
}
