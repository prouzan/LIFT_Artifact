#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand() % 2;
}

int main() {
    int _r, da, db, temp;
    scanf("%d", &_r);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    if (_r >= 0) {
		da = 2 * _r;
		db = 2 * _r;
		while (da >= _r) {
            printf("%d\n", _r);
			if (_nondet_2()) {
printf("L1\n");
				da = da - 1;
			} else {
printf("L2\n");
				da = db - 1;
				db = da;
			}
		}
	}
	return 0;
}
