/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 15:43:19 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/13 15:43:19 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#ifndef HEADER_H
# define HEADER_H

# define BUFFER_SIZE	1
# define FLAG_BENCH		1	// 00001
# define FLAG_SIMPLE	2	// 00010
# define FLAG_MEDIUM	4	// 00100
# define FLAG_COMPLEXE	8	// 01000
# define FLAG_ADAPTIVE	16	// 10000

# include <unistd.h>
# include <stdlib.h>
# include <stdarg.h>
# include <string.h>
# include <stdbool.h>
# include <limits.h>

# include <stdio.h>
typedef	struct s_node
{
	int				value;
	unsigned int	index;
	struct s_node	*next;
	struct s_node	*previous;
}					t_node;

typedef struct s_stack
{
	t_node	*head;
	int		size;
}			t_stack;

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

char	**ft_split(char const *s, char c);
char	**free_split(char **split, int indx, int flag);

int		ft_check_flag(char **av, int *i);
int		ft_strncmp(char *s1, char *s2, size_t n);
int		ft_atoi(const char *str, int *nbr);

size_t	ft_strlen(char *str);

void	ft_safe_write(int fd, char *str, int len);
t_stack	parsing(int *ac, char **av);

#endif
