/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   gnl_utils.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 01:40:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/24 09:08:07 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

char	*ft_strjoin(char *s1, char s2[])
{
	char	*str;
	char	*tmp;
	size_t	i;

	i = 0;
	tmp = s1;
	str = malloc((ft_strlen(s1) + ft_strlen(s2) + 1) * sizeof(char));
	if (!str)
	{
		free(s1);
		return (NULL);
	}
	while (*s1)
		str[i++] = *s1++;
	while (*s2)
		str[i++] = *s2++;
	free(tmp);
	str[i] = 0;
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
	if (!line || !*line)
		return ;
	i = ft_check_line(*line) + 1;
	if (i == 0)
		return ;
	while (j < BUFFER_SIZE && (*line)[i + ++j])
		buffer[j] = (*line)[i + j];
	while ((*line)[i])
		(*line)[i++] = 0;
	buffer[j] = 0;
}
