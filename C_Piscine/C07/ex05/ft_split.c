#include <stdio.h>
#include <stdlib.h>

int	is_sep(char c, char *charset)
{
	int	i;

	i = 0;
	if (c == 0)
		return (1);
	while (charset[i])
	{
		if (c == charset[i])
			return (1);
		i++;
	}
	return (0);
}

int	count_words(char *str, char *charset)
{
	int	i;
	int	words;
	
	i = 0;
	words = 0;
	while (str[i])
	{
		if (!is_sep(str[i], charset) && is_sep(str[i + 1], charset))
			words ++;
		i++;
	}
	return (words);
}

void	ft_strcpy(char *dest, char *src, char *charset)
{
	int	i;

	i = 0;
	while (!is_sep(src[i], charset))
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = 0;
}

void	alloc_split(char **split, char *str, char *charset)
{
	int	words;
	int	i;
	int	j;

	i = 0;
	words = 0;
	while (str[i])
	{
		if (is_sep(str[i], charset))
			i++;
		else
		{
			j = 0;
			while (!is_sep(str[i + j], charset))
				j++;
			split[words] = malloc((j + 1) * sizeof(char));
			ft_strcpy(split[words], (str + i), charset); 
			i += j;
			words++;
		}
	}
}

char	**ft_split(char *str, char *charset)
{
	char	**split;
	int		words;

	words = count_words(str, charset);
	split = malloc((words + 1) * sizeof(char *));
	alloc_split(split, str, charset);
	split[words] = 0;
	return (split);
}

/*
int	main(void)
{
	char	str[] = "///salut comment/sa,va";
	char	charset[] = "/ ";
	char	**split;
	int		i;

	i = 0;
	split = ft_split(str, charset);
	while (split[i])
	{
		printf("%s\n", split[i]);
		i++;
	}
}
*/
