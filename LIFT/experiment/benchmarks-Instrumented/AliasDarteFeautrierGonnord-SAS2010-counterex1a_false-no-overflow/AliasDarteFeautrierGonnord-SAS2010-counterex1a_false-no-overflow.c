#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
    int x, y, n, b;
    scanf("%d%d%d%d", &n, &b, &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (x >= 0 && 0 <= y && y <= n) {
        printf("x:%d,y:%d,n:%d,b:%d\n", x, y, n, b);
		if (b == 0) {
			y = y + 1;
			if (_nondet_2()) {
				b = 1;
      }
		} else {
			y = y - 1;
			if (_nondet_2()) {
				x = x - 1;
				b = 0;
			}
		}
	}
	return 0;
}
