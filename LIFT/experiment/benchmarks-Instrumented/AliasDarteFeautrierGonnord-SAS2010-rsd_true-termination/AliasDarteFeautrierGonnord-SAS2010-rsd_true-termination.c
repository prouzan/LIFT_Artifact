#include <stdio.h>
#include <stdlib.h>

int _nondet_2() {
    return rand() % 2;
}

int main() {
    int _r, da, db, temp;
    scanf("%d", &_r);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    if (_r >= 0) {
		da = 2 * _r;
		db = 2 * _r;
		while (da >= _r) {
            printf("_r:%d,da:%d,db:%d,temp:%d\n", _r, da, db, temp);
			if (_nondet_2()) {
				da = da - 1;
			} else {
				da = db - 1;
				db = da;
			}
		}
	}
	return 0;
}
