#include <stdio.h>

int main()
{
  int a;
  scanf("%d", &a);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (a > 1)
  {
    printf("a:%d\n", a);

    if (a % 10 == 0)
      a = a / 10;
    else
      a = a - 1;
  }
  return 0;
}
