#include <stdio.h>

int main()
{
  int m, n, v1, v2;
  scanf("%d%d", &n, &m);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  if (n >= 0 && m > 0)
  {
    v1 = n;
    v2 = 0;
    while (v1 > 0)
    {
      printf("m:%d,n:%d,v1:%d,v2:%d\n", m, n, v1, v2);
      if (v2 < m)
      {
        v2 = v2 + 1;
        v1 = v1 - 1;
      }
      else
      {
        v2 = 0;
      }
    }
  }
  return 0;
}
