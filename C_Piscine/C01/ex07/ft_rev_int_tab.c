#include <stdio.h>

void ft_rev_int_tab(int *tab, int size)
{
  int i = 0;
  int tmp = 0;

  size--;
  while (i < size)
  {
    tmp = tab[i];
    tab[i] = tab[size];
    tab[size] = tmp;
    i++;
    size--;
  }
}

/*
int main(void)
{
  int tab[4] = {1, 2, 3, 4};
  int i = 0;

  ft_rev_int_tab(tab, 4);
  while (i < 4)
  {
    printf("%d\n", tab[i]);
    i++;
  }
}
*/
