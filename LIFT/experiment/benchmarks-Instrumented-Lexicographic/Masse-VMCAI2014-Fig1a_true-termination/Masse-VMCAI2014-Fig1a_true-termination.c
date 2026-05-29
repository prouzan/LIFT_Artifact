#include <stdio.h>

int main() {
	int a, b;
	scanf("%d%d", &a, &b);
	printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
	while (a >= 0) {
		printf("%d,%d\n", a, b);
		a = a + b;
		if (b >= 0) {
printf("L1\n");
			b = -b - 1;
		} else {
printf("L2\n");
			b = -b;
		}
	}
	return 0;
}
