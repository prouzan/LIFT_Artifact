#include <stdio.h>

int main()
{
  int a, b;
  scanf("%d%d", &a, &b);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (a > b)
  {
    printf("a:%d,b:%d\n", a, b);
    b = b + a;
    a = a + 1;
  }
  return 0;
}
