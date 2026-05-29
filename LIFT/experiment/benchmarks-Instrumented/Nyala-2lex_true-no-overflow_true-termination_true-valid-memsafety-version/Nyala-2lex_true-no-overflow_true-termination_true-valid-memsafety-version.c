#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
	return rand()%200 - 100;
}

int main() {
	int x, y;
	scanf("%d%d", &x, &y);
	printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
	while (x > 0 && y > 0) {
		printf("x:%d,y:%d\n", x, y);
		y = y - x;
		if (y < 0) {
			x = x - 1;
			y = _nondet_int();
		}
	}
  	return 0;
}
