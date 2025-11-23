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

#include "get_next_line.h"
#include <string.h>

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

void	ft_double_check(char **line, char buffer[])
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

char	*ft_get_line(int fd, char *line, char buffer[])
{
	long	bytes_read;

	bytes_read = 1;
	if (!line)
		return (NULL);
	while (ft_check_line(line) == -1 && bytes_read != 0)
	{
		bytes_read = read(fd, buffer, BUFFER_SIZE);
		if (bytes_read < 0)
		{
			buffer[0] = 0;
			free(line);
			return (NULL);
		}
		buffer[bytes_read] = 0;
		line = ft_strjoin(line, buffer);
		if (!line)
			return (NULL);
	}
	if (bytes_read == 0)
		return (NULL);
	return (line);
}

char	*get_next_line(int fd)
{
	static char	buffer[BUFFER_SIZE + 1];
	char	*line;

	line = malloc(sizeof(char));
	if (!line)
		return (NULL);
	if (fd < 0 || BUFFER_SIZE <= 0)
	{
		free(line);
		return (NULL);
	}
	line = ft_strjoin(line, buffer);
	line = ft_get_line(fd, line, buffer);
	if (!line)
	{
		free(line);
		return (NULL);
	}
	ft_double_check(&line, buffer);
	return (line);
}

int	main(int ac, char **av)
{
	int	i;
	int	fd;
	char	*line;

	i = 0;
	fd = 0;
	line = NULL;
	if (ac == 2)
	{
		fd = open(av[1], O_RDONLY);
		if (fd == -1)
			return (-1);
	}
	line = get_next_line(fd);
	while (line && i < 99)
	{
		printf("%d: %s", i, line);
		line = get_next_line(fd);
		i++;
	}
	free(line);
}
