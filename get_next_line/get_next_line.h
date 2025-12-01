/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 15:05:26 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/25 11:20:01 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H
# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 32
# endif
# include <stdlib.h>
# include <unistd.h>

size_t	ft_strlen(char *str);
char	*ft_strjoin(char *s1, char s2[]);
int		ft_check_line(char *line);
void	ft_format(char **line, char buffer[]);
char	*get_next_line(int fd);

#endif
