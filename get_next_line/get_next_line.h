/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 15:05:26 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/21 15:10:08 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H
#ifndef BUFFER_SIZE
# define BUFFER_SIZE 32
#endif
# include <stdlib.h>
# include <unistd.h>
# include <fcntl.h>
# include <stdio.h>
# include <stddef.h>

typedef struct	s_list
{
	char		buffer[BUFFER_SIZE + 1];
	int		fd;
	struct s_list	*next;
}	t_list;

void	ft_bzero(void *s, size_t n);
size_t	ft_strlen(char *str);
char	*ft_strjoin(char *s1, char s2[]);
int	ft_check_line(char *line);
void	ft_format(char **line, char buffer[]);
void	ft_lstadd_back(t_list **lst, int fd);
char	*get_next_line(int fd);

#endif
