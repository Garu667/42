#include <stdlib.h>
#include <stdio.h>

int	ft_strlen(char *str)
{
	int i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*ft_strdup(char *str)
{
	int	i;
	int	str_len = ft_strlen(str);
	char	*dup;

	i = 0;
	dup = malloc((str_len + 1) * sizeof(char));
	while (str[i])
	{
		dup[i] = str[i];
		i++;
	}
	dup[str_len] = 0;
	return (dup);
}
/*
int main(void)
{
	char	str[] = "salut";
	char	*dup;
	dup = ft_strdup(str);
	printf("%d\t", ft_strlen(str));
	printf("%s\n", dup);
}
*/
