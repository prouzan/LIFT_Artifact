#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
	int x;
	scanf("%d", &x);
	printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
	while (x <= 100) {
		printf("x:%d\n", x);
		if (_nondet_2() != 0) {
			x = -2*x + 2;
		} else {
			x = -3*x - 2;
		}
	}
	return 0;
}
