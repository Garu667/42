/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   split.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:33:27 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:33:27 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static int	count_words(char const *s, char c)
{
	int	i;
	int	words;

	i = -1;
	words = 0;
	while (s[++i])
	{
		if ((s[i] != c && s[i] != 0) && (s[i + 1] == c || s[i + 1] == 0))
			words++;
	}
	return (words);
}

static void	ft_strcpy(char *dest, char const *s, char c)
{
	int	i;

	i = -1;
	while (s[++i] != c && s[i] != 0)
		dest[i] = s[i];
	dest[i] = 0;
}

static int	alloc_split(char **split, char const *s, char c)
{
	int	words;
	int	i;
	int	j;

	i = 0;
	words = 0;
	while (s[i])
	{
		if (s[i] == c || s[i] == 0)
			i++;
		else
		{
			j = 0;
			while (s[i + j] != c && s[i + j] != 0)
				j++;
			split[words] = malloc((j + 1) * sizeof(char));
			if (!split[words])
				return (words);
			ft_strcpy(split[words], (s + i), c);
			i += j;
			words++;
		}
	}
	return (-1);
}

char	**ft_split(char const *s, char c)
{
	char	**split;
	int		words;
	int		ret;

	ret = 0;
	words = count_words(s, c);
	split = malloc((words + 1) * sizeof(char *));
	if (!split)
		return (NULL);
	ret = alloc_split(split, s, c);
	if (ret != -1)
	{
		free_all(NULL, split, 2);
		return (NULL);
	}
	split[words] = 0;
	return (split);
}
