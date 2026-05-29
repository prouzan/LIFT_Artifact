#include <stdio.h>

int main() {
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (x < 0) {
        printf("%d\n", x);
        x = -3*x - 17;
    }
    return 0;
}
