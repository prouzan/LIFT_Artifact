#include <stdio.h>

int main() {
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (x > 0) {
        printf("x:%d\n", x);
        x = -2*x + 10;
    }
    return 0;
}
