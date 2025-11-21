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

size_t	ft_strlen(char *str);
char	*ft_strjoin(char *s1, char s2[]);
/*
typedef struct s_fd_data
{
	struct s_fd_data	*next;
	char				*rest;
	int					fd;
}	t_fd_data;
*/

#endif
