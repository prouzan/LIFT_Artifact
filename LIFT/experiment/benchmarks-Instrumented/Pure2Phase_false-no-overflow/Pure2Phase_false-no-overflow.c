#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
	return rand() % 200 - 100;
}

int main() {
	int y, z;
	scanf("%d%d", &y, &z);
	printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
	while (z >= 0) {
		printf("y:%d,z:%d\n", y, z);
		y = y - 1;
		if (y >= 0) {
			z = _nondet_int();
		} else {
			z = z - 1;
		}
	}
	return 0;
}
