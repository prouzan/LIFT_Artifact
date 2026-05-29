#include <stdio.h>

int main()
{
  int a, b, olda;
  scanf("%d%d", &a, &b);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (a > 0) {
    printf("a:%d,b:%d,olda:%d\n", a, b, olda);
    olda = a;
    a = 3*olda - 4*b;
    b = 4*olda + 3*b;
  }
  return 0;
}
