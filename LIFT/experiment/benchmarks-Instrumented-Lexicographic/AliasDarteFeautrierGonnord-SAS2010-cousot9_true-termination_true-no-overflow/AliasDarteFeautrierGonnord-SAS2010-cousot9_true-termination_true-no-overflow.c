#include <stdio.h>

int main() {
    int _i, j, N;
    scanf("%d%d", &j, &N);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    _i = N;
    while (_i > 0) {
        printf("%d,%d\n", j, N);
		if (j > 0) {
printf("L1\n");
			j = j - 1;
		} else {
printf("L2\n");
			j = N;
			_i = _i - 1;
		}
	}
	return 0;
}
