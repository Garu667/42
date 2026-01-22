/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 15:43:19 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/22 18:53:47 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef HEADER_H
# define HEADER_H

# define BUFFER_SIZE	1
# define FLAG_BENCH		1
# define FLAG_SIMPLE	2
# define FLAG_MEDIUM	4
# define FLAG_COMPLEX	8
# define FLAG_ADAPTIVE	16

# include <unistd.h>
# include <stdlib.h>
# include <stdbool.h>
# include <limits.h>

typedef struct s_node
{
	int				value;
	int				index;
	struct s_node	*next;
	struct s_node	*prev;
}					t_node;

typedef struct s_chunk
{
	int		min;
	int		max;
}			t_chunk;

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

/*--------------------------algorithms----------------------------*/
int		find_min_position(t_stack *a);
int		get_position(t_stack *stack, int index);
void	bring_min_top(t_stack *a, t_stack *b, t_bench *bench);
void	chunk_sort(t_stack *a, t_stack *b, t_bench *bench);
void	radix_sort(t_stack *a, t_stack *b, t_bench *bench);
void	tiny_sort(t_stack *a, t_stack *b, t_bench *bench);
void	selection_sort(t_stack *a, t_stack *b, t_bench *bench);
/*--------------------------operations----------------------------*/
int		pa(t_stack *a, t_stack *b, bool write_switch);
int		pb(t_stack *a, t_stack *b, bool write_switch);
int		ra(t_stack *b, bool write_switch);
int		rb(t_stack *b, bool write_switch);
int		rr(t_stack *a, t_stack *b, bool write_switch);
int		rra(t_stack *a, bool write_switch);
int		rrb(t_stack *b, bool write_switch);
int		rrr(t_stack *a, t_stack *b, bool write_switch);
int		sa(t_stack *a, bool write_switch);
int		sb(t_stack *b, bool write_switch);
int		ss(t_stack *a, t_stack *b, bool write_switch);
/*----------------------------split-------------------------------*/
char	**free_split(char **split, int indx, int flag);
char	**ft_split(char const *s, char c);
/*----------------------------check-------------------------------*/
int		ft_check_flag(char **av, int *i);
void	free_stack(t_stack *stack);
/*----------------------------index-------------------------------*/
void	stack_to_index(t_stack *a);
/*---------------------------parsing------------------------------*/
t_stack	parsing(int *ac, char **av);
/*---------------------------benchmark----------------------------*/
float	ft_compute_disorder(t_stack stack);
void	do_op_bench(t_stack *a, t_stack *b, t_bench *bench, char *op);
void	do_op_nobench(t_stack *a, t_stack *b, t_bench *bench, char *op);
void	print_benchmark(t_bench *bench);
void	setup_benchmark(t_bench *bench, float disorder, int flag);
/*-----------------------------gnl--------------------------------*/
char	*ft_strjoin(char *s1, char s2[]);
char	*get_next_line(int fd);
int		ft_check_line(char *line);
void	ft_format(char **line, char buffer[]);
/*----------------------------utils-------------------------------*/
bool	is_sorted(t_stack *a);
char	*ft_strtrim(char *s1, char *set);
int		ft_atoi(const char *str, int *nbr);
int		ft_putstr_fd(char *s, int fd);
int		ft_strncmp(char *s1, char *s2, size_t n);
size_t	ft_strlen(char *str);
void	ft_safe_write(int fd, char *str, int len);
void	ft_putnbr_fd(int n, int fd);

#endif
