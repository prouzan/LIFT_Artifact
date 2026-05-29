#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
	return rand() % 200 - 100;
}

int main() {
	int y, z;
	scanf("%d%d", &y, &z);
	printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
	while (z >= 0) {
		printf("%d,%d\n", y, z);
		y = y - 1;
		if (y >= 0) {
printf("L1\n");
			z = _nondet_int();
		} else {
printf("L2\n");
			z = z - 1;
		}
	}
	return 0;
}
