#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}
int _nondet_3() {
    return rand()%3;
}

int main() {
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (x <= 100) {
        printf("x:%d\n", x);
        if (0 == _nondet_3()) {
            x = - 2 * x + 2;
        } else if (0 == _nondet_2()) {
            x = - 3 * x - 2;
        } else {
            x = - 4 * x + 2;
        }
    }
}
