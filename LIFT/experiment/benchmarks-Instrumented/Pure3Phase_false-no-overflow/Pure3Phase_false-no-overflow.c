#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
    int x, y, z;
    scanf("%d%d%d", &x, &y, &z);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (x >= 0) {
        printf("x:%d,y:%d,z:%d\n", x, y, z);
        if (_nondet_2() != 0) {
            x = x + y;
        } else {
            x = x + z;
        }
        y = y + z;
        z = z - 1;
    }
    return 0;
}
