#include <stdio.h>

int is_sep(char c)
{
  if ((c >= 58 && c <= 64) || (c >= 91 && c <= 96) || c >= 123 || c <= 47)
    return (1);

  return (0);
}


int is_ok(char *str, int i)
{
  int j = 0;
  j = i;
  while (!is_sep(str[j]))
    j++;
  return (j);
}

char *ft_strcapitalize(char *str)
{
  int i = 0;
  int j = 0;

  while (str[i])
  {
    j = -1;
    if (!is_sep(str[i]))
      j = is_ok(str, i);
    if (j > 0)
    {
      if (str[i] >= 97 && str[i] <= 122)
        str[i] -= 32;
      while (!is_sep(str[i]))
      {
        i++;
        if (str[i] >= 65 && str[i] <= 90)
          str[i] += 32;
      }
      i = j;
    }
    else
      i++;
  }
  return (str);
}

/*
int main(void)
{
  //char str[] = "salut, comment tu vas ? 42mots quarante-deux; cinquante+et+un";
  char str[] = "HELLO";
  int sp = 0;
  printf("%s\n", str);
  printf("%s\n", ft_strcapitalize(str));
}
*/
