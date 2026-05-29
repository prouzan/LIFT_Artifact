#include <stdio.h>

int main() {
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (x < 0) {
        printf("x:%d\n", x);
        x = -3*x - 17;
    }
    return 0;
}
