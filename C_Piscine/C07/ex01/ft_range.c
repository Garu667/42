#include <stdlib.h>
#include <stdio.h>

int *ft_range(int min, int max)
{
  int *tab;
  int i = 0;
  if (min >= max)
    return NULL;
  tab = malloc((max - min) * sizeof(int));
  while (min < max)
  {
    tab[i] = min;
    i++;
    min++;
  }
  return (tab);
}
/*
int main(void)
{
  int *tab;
  tab = ft_range(4, 8);
  int i = 0;
  while (i != 5)
  {
    printf("%d\t", tab[i]);
    i++;
  }
}
*/
