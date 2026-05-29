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
	printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
	while (x != 0 && y > 0) {
		printf("%d,%d\n", x, y);
    if (x > 0) {
printf("L1\n");
      if (_nondet_2() != 0) {
printf("L2\n");
			    x = x - 1;
          y = _nondet_int();
			} else {
printf("L3\n");
			    y = y - 1;
			}
		} else {
printf("L4\n");
      if (_nondet_2() != 0) {
printf("L5\n");
			    x = x + 1;
			} else {
printf("L6\n");
			    y = y - 1;
          x = _nondet_int();
			}
		}
	}
  	return 0;
}
