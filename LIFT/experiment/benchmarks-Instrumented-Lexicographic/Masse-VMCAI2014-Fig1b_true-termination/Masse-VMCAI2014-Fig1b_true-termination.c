#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand()%2;
}

int main() {
	int x;
	scanf("%d", &x);
	printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
	while (x <= 100) {
		printf("%d\n", x);
		if (_nondet_2() != 0) {
printf("L1\n");
			x = -2*x + 2;
		} else {
printf("L2\n");
			x = -3*x - 2;
		}
	}
	return 0;
}
