#include <stdio.h>

int main() {
    int _i, j, N;
    scanf("%d%d", &j, &N);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    _i = N;
    while (_i > 0) {
        printf("_i:%d,j:%d,N:%d\n", _i, j, N);
		if (j > 0) {
			j = j - 1;
		} else {
			j = N;
			_i = _i - 1;
		}
	}
	return 0;
}
