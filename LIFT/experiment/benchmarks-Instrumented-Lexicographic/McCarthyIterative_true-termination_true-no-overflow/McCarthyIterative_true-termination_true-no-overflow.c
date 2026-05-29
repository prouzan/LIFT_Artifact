#include <stdio.h>

int main() {
    int x;
    int c;
    scanf("%d", &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    c = 1;

    while (c > 0) {
        printf("%d\n", x);
        if (x > 100) {
printf("L1\n");
            x = x-10;
            c = c-1;
        } else {
printf("L2\n");
            x = x+11;
            c = c+1;
        }
    }

    return 0;
}
