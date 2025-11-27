/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_bonus.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 14:47:45 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/25 14:46:20 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line_bonus.h"

int	ft_manage_list(t_list **lst, int fd)
{
	t_list	*node;
	int		i;

	i = 0;
	if (!*lst)
	{
		if (ft_lstadd_back(lst, fd) == -1)
			return (-1);
		return (i);
	}
	node = *lst;
	while (node)
	{
		if (node->fd == fd)
			return (i);
		node = node->next;
		i++;
	}
	if (ft_lstadd_back(lst, fd) == -1)
		return (-1);
	return (i);
}

void	ft_delnode(t_list **lst, int fd)
{
	t_list	*node;
	t_list	*behind_node;

	node = *lst;
	behind_node = NULL;
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
	while (ft_check_line(line) == -1 && bytes_read != 0)
	{
		bytes_read = read(fd, buffer, BUFFER_SIZE);
		if (bytes_read < 0)
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
	if (ft_strlen(line) == 0)
	{
		ft_delnode(lst, fd);
		free(line);
		return (NULL);
	}
	return (line);
}

char	*get_next_line(int fd)
{
	static t_list	*lst;
	t_list			*node;
	char			*line;
	char			*tmp;

	if (fd < 0 || BUFFER_SIZE <= 0 || ft_manage_list(&lst, fd) == -1)
		return (NULL);
	node = lst;
	while (node && node->fd != fd)
		node = node->next;
	line = malloc(sizeof(char));
	if (!line)
		return (ft_delnode(&lst, node->fd), NULL);
	line[0] = 0;
	tmp = line;
	line = ft_strjoin(line, node->buffer);
	if (!line)
		return (ft_delnode(&lst, node->fd), free(tmp), NULL);
	line = ft_get_line(&lst, node->fd, line, node->buffer);
	if (!line)
		return (NULL);
	ft_format(&line, node->buffer);
	if (node->buffer[0] == 0)
		ft_delnode(&lst, node->fd);
	return (line);
}
/*
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int     i;
    int        j;
    int     fd;
    char    *line;

    j = 0;
    if (argc < 2)
    {
        printf("Usage: %s <file1> [file2...]\n", argv[0]);
        return (1);
    }

    i = 1;
    while (i < argc)
    {
        fd = open(argv[i], O_RDONLY);
        if (fd < 0)
        {
            perror("open");
            i++;
            continue;
        }
        printf("=== Lecture du fichier %s ===\n", argv[i]);
        while ((line = get_next_line(fd)) != NULL && j < 5)
        {
            printf("%s", line);
	    j++;
            free(line);
        }
        j = 0;
        close(fd);
        i++;
        printf("\n");
    }
    return (0);
}
*/
