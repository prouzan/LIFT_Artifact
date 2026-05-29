#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
    int x, y, n, b;
    scanf("%d%d%d%d", &n, &b, &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (x >= 0 && 0 <= y && y <= n) {
        printf("%d,%d,%d,%d\n", n, b, x, y);
		if (b == 0) {
printf("L1\n");
			y = y + 1;
			if (_nondet_2()) {
printf("L2\n");
				b = 1;
      }
		} else {
printf("L3\n");
			y = y - 1;
			if (_nondet_2()) {
printf("L4\n");
				x = x - 1;
				b = 0;
			}
		}
	}
	return 0;
}
