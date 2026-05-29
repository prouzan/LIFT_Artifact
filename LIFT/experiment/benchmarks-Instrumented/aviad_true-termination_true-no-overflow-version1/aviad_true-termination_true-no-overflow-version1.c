#include <stdio.h>

int main()
{
  int a;
  scanf("%d", &a);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (a > 1)
  {
    printf("a:%d\n", a);

    if (a % 2 == 0)
      a = a / 2;
    else if (a % 3 == 0)
      a = a / 3;
    else
      a = a + 1;
  }
  return 0;
}
