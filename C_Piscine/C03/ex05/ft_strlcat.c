#include <stdio.h>
#include <string.h>

int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

unsigned int		ft_strlcat(char *dst, char *src, unsigned int size)
{
	unsigned int		i;
	unsigned int		t1;
	unsigned int		t2;

	i = 0;
	t1 = ft_strlen(dst);
	t2 = ft_strlen(src);
	if ((size - 1) <= t1)
		return (t2 + size);
	while (t1 + i < (size - 1))
	{
		dst[t1 + i] = src[i];
		i++;
	}
	dst[t1 + i] = 0;
	return (t1 + t2);
}
/*
int	main(void)
{
	char	dst[] = "Salutbbbbbb";
	char	src[] = "aaaaaaaa";
	printf("%d\t", ft_strlcat(dst, src, 6));
	printf("%s\t%s\n", dst, src);
	char	dst2[] = "Salutbbbbb";
	char	src2[] = "aaaaaaa";
	printf("%d\t", strlcat(dst2, src2, 6));
	printf("%s\t%s\n", dst2, src2);
}
*/
