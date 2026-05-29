#include <stdio.h>

int main()
{
  int a, b;
  scanf("%d%d", &a, &b);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (a > b)
  {
    printf("%d,%d\n",a,b);
    b = b + a;
    a = a + 1;
  }
  return 0;
}
