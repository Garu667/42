#include <unistd.h>

void ft_putstr(char *str)
{
  while (*str)
  {
    write(1, &*str, 1);
    str++;
  }
}

/*
int main(int ac, char **av)
{
  if (ac != 2)
  {
    return 0;
  }
  ft_putstr(av[1]);
}
*/
