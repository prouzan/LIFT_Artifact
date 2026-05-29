#include <stdio.h>
#include <stdlib.h>

int _nondet_4() {
    return rand()%4;
}
int _nondet_3() {
    return rand()%3;
}
int _nondet_2() {
    return rand()%2;
}

int main() {
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (x <= 100) {
        printf("%d\n", x);
        if (0 == _nondet_4()) {
printf("L1\n");
            x = - 2 * x + 2;
        } else if (0 == _nondet_3()) {
printf("L2\n");
            x = - 3 * x - 2;
        } else if (0 == _nondet_2()) {
printf("L3\n");
            x = - 4 * x + 2;
        } else {
printf("L4\n");
            x = - 5 * x - 2;
        }
    }
}
