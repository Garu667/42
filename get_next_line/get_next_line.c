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

int	ft_manage_list(t_list **lst, int fd)
{
	t_list	*node;
	int	i;

	i = 0;
	node = *lst;
	if (!node)
	{
		node = malloc(sizeof(t_list));
		if (!node)
			return (-1);
		node->fd = fd;
		node->next = NULL;
		*lst = node;
		return (i);
	}
	while (node)
	{
		if (node->fd == fd)
			return (i);
		node = node->next;
		i++;
	}
	ft_lstadd_back(lst, fd);
	return (i);
}

void	ft_delnode(t_list **lst, int fd)
{
	t_list	*node;
	t_list	*behind_node;

	node = *lst;
	while (node)
	{
		if (node->fd == fd)
		{
			if (behind_node)
				behind_node->next = node->next;
			else
				*lst = node->next;
			free(node);
			return ;
		}
		behind_node = node;
		node = node->next;
	}
}

char	*ft_get_line(t_list **lst, int fd, char *line, char buffer[])
{
	long	bytes_read;

	bytes_read = 1;
	if (!line)
		return (NULL);
	while (ft_check_line(line) == -1 && bytes_read != 0)
	{
		bytes_read = read(fd, buffer, BUFFER_SIZE);
		if (bytes_read <= 0)
		{
			ft_delnode(lst, fd);
			free(line);
			return (NULL);
		}
		buffer[bytes_read] = 0;
		line = ft_strjoin(line, buffer);
		if (!line)
			return (NULL);
	}
	return (line);
}

char	*get_next_line(int fd)
{
	static t_list	*lst;
	char	*line;
	int	i;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	i = ft_manage_list(&lst, fd);
	line = malloc(sizeof(char));
	if (!line || i == -1)
		return (NULL);
	line[0] = 0;
	line = ft_strjoin(line, lst[i].buffer);
	if (!line)
	{
		free(line);
		return (NULL);
	}
	line = ft_get_line(&lst, fd, line, lst[i].buffer);
	if (!line)
		return (NULL);
	ft_format(&line, lst[i].buffer);
	return (line);
}

int	main(int ac, char **av)
{
	int	i;
	int	fd1;
	int	fd2;
	char	*line;

	i = 0;
	fd1 = open(av[1], O_RDONLY);
	fd2 = open(av[2], O_RDONLY);
	while (++i < 6)
	{
		line = get_next_line(fd1);
		printf("%d: %s", fd1, line);
	}
	i = 0;
	while (++i < 6)
	{
		line = get_next_line(fd2);
		printf("%d: %s", fd2, line);
	}
	i = 0;
	while (++i < 6)
	{
		line = get_next_line(fd1);
		printf("%d: %s", fd1, line);
	}
	free(line);
}
