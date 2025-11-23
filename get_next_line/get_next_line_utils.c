/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 15:03:58 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/21 15:10:03 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

void	ft_bzero(void *s, size_t n)
{
	char	*str;
	size_t	i;

	i = 0;
	str = (char *)s;
	while (i < n)
		str[i++] = 0;
}

size_t	ft_strlen(char *str)
{
	size_t	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

char	*ft_strjoin(char *s1, char s2[])
{
	char	*str;
	size_t	i;
	size_t	j;

	i = -1;
	j = ft_strlen(s1);
	str = malloc(sizeof(char) * (ft_strlen(s1) + ft_strlen(s2) + 1));
	if (!str)
		return (NULL);
	while (s1[++i])
		str[i] = s1[i];
	i = 0;
	while (s2[i])
		str[j++] = s2[i++];
	str[j] = 0;
	return (str);
}

int	ft_check_line(char *line)
{
	int	i;

	i = -1;
	if (!line || line[0] == 0)
		return (-1);
	while (line[++i])
		if (line[i] == '\n')
			return (i);
	return (-1);
}

void	ft_format(char **line, char buffer[])
{
	int	i;
	int	j;

	j = -1;
	i = ft_check_line(*line) + 1;
	if (i == 0)
		return ;
	while ((*line)[i + ++j] && j != BUFFER_SIZE)
		buffer[j] = (*line)[i + j];
	buffer[j] = 0;
	(*line)[i] = 0;
}
