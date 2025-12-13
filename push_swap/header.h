/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: bcondemi <bcondemi@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 12:57:23 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/11 14:57:37 by bcondemi         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef HEADER_H
# define HEADER_H

# define BUFFER_SIZE 1
# define FLAG_BENCH    1	// 00001
# define FLAG_SIMPLE   2	// 00010
# define FLAG_MEDIUM   4	// 00100
# define FLAG_COMPLEXE 8	// 01000
# define FLAG_ADAPTIVE 16	// 10000
# include <unistd.h>
# include <stdlib.h>
# include <stdarg.h>
# include <string.h>
# include <stdbool.h>
# include <limits.h>

typedef struct s_stack
{
	int		*tab;
	int		size;
}	t_stack;

typedef struct s_bench
{
	float	disorder;
	int		strats;
	int		ops[11];
	void	(*op)(t_stack *a, t_stack *b, struct s_bench *bench, char *op);
}	t_bench;

/*-------------operation-------------*/
int		sa(t_stack *a, bool write_switch);
int		sb(t_stack *b, bool write_switch);
int		ss(t_stack *a, t_stack *b, bool write_switch);
int		pa(t_stack *a, t_stack *b, bool write_switch);
int		pb(t_stack *a, t_stack *b, bool write_switch);
int		ra(t_stack *b, bool write_switch);
int		rb(t_stack *b, bool write_switch);
int		rr(t_stack *a, t_stack *b, bool write_switch);
int		rra(t_stack *a, bool write_switch);
int		rrb(t_stack *b, bool write_switch);
int		rrr(t_stack *a, t_stack *b, bool write_switch);
/*-------------mandatory-------------*/
void	ft_safe_write(int fd, char *str, int len);
int		ft_putstr_fd(char *s, int fd);
int		ft_strncmp(char *s1, char *s2, size_t n);
float	ft_compute_disorder(t_stack stack);
void	parse_one(char *str, t_stack *stack);
void	parse_multiple(char **av, int len, t_stack *stack);
t_stack	parsing(int *ac, char **av, int i);
void	push_swap(t_stack *a, int flag, float disorder);
/*---------------bonus-----------------*/
size_t	ft_strlen(char *str);
char	*ft_strjoin(char *s1, char s2[]);
int		ft_check_line(char *line);
void	ft_format(char **line, char buffer[]);
char	*get_next_line(int fd);

#endif
