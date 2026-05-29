#include <stdio.h>

int main()
{
  int a, b, olda;
  scanf("%d%d", &a, &b);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (a > 0) {
    printf("%d,%d\n", a,b);
    olda = a;
    a = 3*olda - 4*b;
    b = 4*olda + 3*b;
  }
  return 0;
}
