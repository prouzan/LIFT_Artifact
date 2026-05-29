#include <stdio.h>

int main()
{
  int m, n, v1, v2;
  scanf("%d%d", &n, &m);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (n >= 0 && m > 0)
  {
    v1 = n;
    v2 = 0;
    while (v1 > 0)
    {
      printf("%d,%d\n", n, m);
      if (v2 < m)
      {
printf("L1\n");
        v2 = v2 + 1;
        v1 = v1 - 1;
      }
      else
      {
printf("L2\n");
        v2 = 0;
      }
    }
  }
  return 0;
}
