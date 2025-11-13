#include <stdio.h>

int ft_str_is_uppercase(char *str)
{
  int i = 0;
  if (str[0] == 0)
    return 1;
  while (str[i] != 0)
  {
    if (!(str[i] >= 'A' && str[i] <= 'Z'))
      return (0);
    i++;
  }
  return (1);
}
/*
int main(void)
{
  printf("%d\n", ft_str_is_uppercase("Salut"));
}
*/
