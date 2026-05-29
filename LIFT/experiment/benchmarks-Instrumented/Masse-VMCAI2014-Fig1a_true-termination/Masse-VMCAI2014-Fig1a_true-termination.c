#include <stdio.h>

int main() {
	int a, b;
	scanf("%d%d", &a, &b);
	printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
	while (a >= 0) {
		printf("a:%d,b:%d\n", a, b);
		a = a + b;
		if (b >= 0) {
			b = -b - 1;
		} else {
			b = -b;
		}
	}
	return 0;
}
