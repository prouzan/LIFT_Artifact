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
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (((an >= _i && bn >= j) || (an >= _i && bn <= j) || (an <= _i && bn >= j)) && k >= tk + 1) {
        printf("%d,%d,%d,%d,%d,%d\n", _i, j, k, an, bn, tk);
		if (an >= _i && bn >= j) {
printf("L1\n");
			if (_nondet_2()) {
printf("L2\n");
				j = j + k;
				tk = k;
				k = _nondet_int();
			} else {
printf("L3\n");
				_i = _i + 1;
			}
		} else {
printf("L4\n");if (an >= _i && bn <= j) {
printf("L5\n");
			_i = _i + 1;
		} else {
printf("L6\n");if (an <= _i && bn >= j) {
printf("L7\n");
			j = j + k;
			tk = k;
			k = _nondet_int();
		}}}
	}
	return 0;
}
