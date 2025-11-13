#include <stdio.h>

int ft_strcmp(char *s1, char *s2)
{
  int i = 0;
  while (s1[i] && s2[i])
  {
    if (s1[i] != s2[i])
      return (s1[i] - s2[i]);
    i++;
  }
  return (s1[i] - s2[i]);
}
/*
int main(void)
{
  int nb = 0;
  nb = ft_strcmp("salut", "salut");
  printf("%d\n", nb);
}
*/
