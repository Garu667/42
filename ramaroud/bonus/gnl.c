/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 14:47:45 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/21 16:06:13 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "../../header.h"

static char	*ft_free(char *to_free)
{
	free(to_free);
	return (NULL);
}

static char	*clear_line(char *line)
{
	char	*new_line;
	int		i;

	i = 0;
	while (line[i] && line[i] != '\n')
		i++;
	if (line[i] == '\n')
		i++;
	new_line = malloc(i + 1);
	if (!new_line)
	{
		free(line);
		return (NULL);
	}
	i = 0;
	while (line[i] && line[i] != '\n')
	{
		new_line[i] = line[i];
		i++;
	}
	if (line[i] == '\n')
		new_line[i++] = '\n';
	new_line[i] = 0;
	return (new_line);
}

static char	*ft_get_line(int fd, char *line, char buffer[])
{
	long	bytes_read;

	bytes_read = 1;
	while (ft_check_line(line) == -1 && bytes_read != 0)
	{
		bytes_read = read(fd, buffer, BUFFER_SIZE);
		if (bytes_read < 0)
		{
			free(line);
			buffer[0] = 0;
			return (NULL);
		}
		buffer[bytes_read] = 0;
		line = ft_strjoin(line, buffer);
		if (!line)
			return (NULL);
	}
	if (bytes_read == 0 && ft_strlen(line) == 0)
	{
		free(line);
		buffer[0] = 0;
		return (NULL);
	}
	return (line);
}

char	*get_next_line(int fd)
{
	char	buffer[BUFFER_SIZE + 1];
	char	*line;
	char	*new_line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	line = malloc(sizeof(char));
	if (!line)
		return (NULL);
	buffer[0] = 0;
	line[0] = 0;
	line = ft_get_line(fd, line, buffer);
	if (!line)
		return (NULL);
	new_line = clear_line(line);
	if (!new_line)
		return (NULL);
	if (new_line[0] == 0)
		return (ft_free(line));
	ft_format(&line, buffer);
	free(line);
	return (new_line);
}
