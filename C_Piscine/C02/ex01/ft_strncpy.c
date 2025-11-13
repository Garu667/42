char *ft_strncpy(char *dest, char *src, unsigned int n)
{
  int i = 0;
  while (n)
  {
    dest[i] = src[i];
    i++;
    n--;
  }
  return (dest);
}
