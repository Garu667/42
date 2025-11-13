#include <stdio.h>

int ft_strcmp(char *s1, char *s2, unsigned int n)
{
  int i = 0;
  n--;
  while (n != 0)
  {
    if (s1[i] != s2[i])
      return (s1[i] - s2[i]);
    i++;
    n--;
  }
  return (s1[i] - s2[i]);
}
/*
int main(void)
{
  int nb = 0;
  nb = ft_strcmp("salut", "salut", 3);
  printf("%d\n", nb);
}
*/
