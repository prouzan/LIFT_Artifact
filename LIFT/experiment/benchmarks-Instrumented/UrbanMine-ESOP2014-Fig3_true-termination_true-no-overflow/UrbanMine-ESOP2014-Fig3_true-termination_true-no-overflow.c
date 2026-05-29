#include <stdio.h>
#include <stdlib.h>

int _nondet_int() {
	return rand()%100;
}
int _nondet_2() {
	return rand()%2;
}
int main() {
	int x;
	int y;
	scanf("%d%d", &x, &y);
	printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
	while (x != 0 && y > 0) {
		printf("x:%d,y:%d\n", x, y);
    if (x > 0) {
      if (_nondet_2() != 0) {
			    x = x - 1;
          y = _nondet_int();
			} else {
			    y = y - 1;
			}
		} else {
      if (_nondet_2() != 0) {
			    x = x + 1;
			} else {
			    y = y - 1;
          x = _nondet_int();
			}
		}
	}
  	return 0;
}
