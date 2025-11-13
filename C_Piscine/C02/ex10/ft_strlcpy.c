#include <stdio.h>
#include <string.h>

int	ft_strlen(char	*str)
{
	int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

unsigned int	ft_strlcpy(char *dest, char *src, unsigned int size)
{
	int	i;
	int	len;

	i = 0;
	len = ft_strlen(src);
	size--;
	while (src[i] && size != 0)
	{
		dest[i] = src[i];
		size--;
		i++;
	}
	dest[i] = '\0';
	return (len);
}

/*
int	main(void)
{
	int	i;

	char	src[] = "soir";
	char	dest[] = "Bonjour";
	i = ft_strlcpy(dest, src, 5);
	printf("%s\t%d\n", dest, i);

	char	src1[] = "soir";
	char	dest1[] = "Bonjour";
	i = strlcpy(dest1, src1, 5);
	printf("%s\t%d\n", dest1, i);
}
*/
