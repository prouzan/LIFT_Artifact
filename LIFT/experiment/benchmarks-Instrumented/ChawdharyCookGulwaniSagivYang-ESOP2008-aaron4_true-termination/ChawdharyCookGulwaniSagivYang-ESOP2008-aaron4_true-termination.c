#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
    return rand();
}
int _nondet_2() {
  return rand()%2;
}
int main() {
    int _i, j, k, an, bn, tk;
    scanf("%d%d%d%d%d%d", &_i, &j, &k, &an, &bn, &tk);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (((an >= _i && bn >= j) || (an >= _i && bn <= j) || (an <= _i && bn >= j)) && k >= tk + 1) {
        printf("_i:%d,j:%d,k:%d,an:%d,bn:%d,tk:%d\n", _i, j, k, an, bn, tk);
		if (an >= _i && bn >= j) {
			if (_nondet_2()) {
				j = j + k;
				tk = k;
				k = _nondet_int();
			} else {
				_i = _i + 1;
			}
		} else {if (an >= _i && bn <= j) {
			_i = _i + 1;
		} else {if (an <= _i && bn >= j) {
			j = j + k;
			tk = k;
			k = _nondet_int();
		}}}
	}
	return 0;
}
