/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 15:03:58 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/24 19:27:56 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line_bonus.h"

size_t	ft_strlen(char *str)
{
	size_t	i;

	i = 0;
	if (!str)
		return (0);
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
	if (ft_strlen(s1) > 0)
	{
		while (s1[++i])
			str[i] = s1[i];
	}
	i = 0;
	if (ft_strlen(s2) > 0)
	{
		while (s2[i])
			str[j++] = s2[i++];
	}
	free(s1);
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

	j = 0;
	i = ft_check_line(*line) + 1;
	if (i == 0)
		return ;
	while ((*line)[i + j] && j < BUFFER_SIZE)
	{
		buffer[j] = (*line)[i + j];
		j++;
	}
	buffer[j] = 0;
	(*line)[i] = 0;
}

int	ft_lstadd_back(t_list **lst, int fd)
{
	t_list	*node;
	t_list	*last;
	int		i;

	node = malloc(sizeof(t_list));
	if (!node)
		return (-1);
	i = 0;
	while (i <= BUFFER_SIZE)
		node->buffer[i++] = 0;
	node->buffer[0] = 0;
	node->fd = fd;
	node->next = NULL;
	if (!*lst)
	{
		*lst = node;
		return (0);
	}
	last = *lst;
	while (last->next)
		last = last->next;
	last->next = node;
	return (0);
}
