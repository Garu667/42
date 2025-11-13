#include <stdlib.h>
#include <stdio.h>

int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	if (str == NULL)
		return (0);
	while (str[i])
		i++;
	return (i);
}

int	ft_strslen(char **strs)
{
	int	i = 0;
	int	len = 0;
	while (strs[i])
	{
		len += ft_strlen(strs[i]);
		i++;
	}
	return (len);
}

char	*ft_strjoin(int size, char **strs, char *sep)
{
	int	sep_len = ft_strlen(sep);
	int	str_len = ft_strslen(strs);
	char	*str;
	int	k = 0;

	if (size == 0)
		return (NULL);
	str = malloc((str_len + (sep_len * (size - 1)) + 1) * sizeof(char));
	if (!str)
		return (NULL);
	str[(str_len + (sep_len * (size - 1)))] = 0;
	while (*strs && size != 0)
	{
		while (**strs)
		{
			str[k] = **strs;
			(*strs)++;
			k++;
		}
		if (size == 1)
			sep += sep_len;
		while (*sep)
		{
			str[k] = *sep;
			k++;
			sep++;
		}
		sep -= sep_len;
		strs++;
		size--;
	}
	return (str);
}
int	main(int ac, char **av)
{
	char	*str;
	str = ft_strjoin(1, av, "-");
	printf("%s\n", str);
}
