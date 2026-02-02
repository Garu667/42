/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:32:28 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:32:28 by ramaroud         ###   ########lyon.fr   */
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
	float	disorder;
	int		size;
}			t_stack;

typedef struct s_bench
{
	float	disorder;
	int		strats;
	int		ops[11];
	void	(*op)(t_stack *a, t_stack *b, struct s_bench *bench, char *op);
}	t_bench;

/*---------------------------------operations---------------------------------*/
int		ra(t_stack *b, bool write_switch);
int		rb(t_stack *b, bool write_switch);
int		sa(t_stack *a, bool write_switch);
int		sb(t_stack *b, bool write_switch);
int		rra(t_stack *a, bool write_switch);
int		rrb(t_stack *b, bool write_switch);
int		ss(t_stack *a, t_stack *b, bool write_switch);
int		pa(t_stack *a, t_stack *b, bool write_switch);
int		pb(t_stack *a, t_stack *b, bool write_switch);
int		rr(t_stack *a, t_stack *b, bool write_switch);
int		rrr(t_stack *a, t_stack *b, bool write_switch);
/*---------------------------------algorithms---------------------------------*/
bool	is_sorted(t_stack *a);
void	stack_to_index(t_stack *a);
int		find_min_position(t_stack *a);
float	ft_compute_disorder(t_stack stack);
int		get_position(t_stack *stack, int index);
void	tiny_sort(t_stack *a, t_stack *b, t_bench *bench);
void	chunk_sort(t_stack *a, t_stack *b, t_bench *bench);
void	radix_sort(t_stack *a, t_stack *b, t_bench *bench);
void	bring_min_top(t_stack *a, t_stack *b, t_bench *bench);
void	selection_sort(t_stack *a, t_stack *b, t_bench *bench);
/*---------------------------------utils--------------------------------------*/
size_t	ft_strlen(char *str);
void	ft_putnbr_fd(int n, int fd);
int		ft_putstr_fd(char *s, int fd);
int		ft_atoi(const char *str, int *nbr);
int		ft_strncmp(char *s1, char *s2, size_t n);
void	ft_safe_write(int fd, char *str, int len);
int		free_all(t_stack *stack, char **split, int flag);
/*---------------------------------benchmark----------------------------------*/
void	print_benchmark(t_bench *bench, t_stack *a);
void	setup_benchmark(t_bench *bench, float disorder, int flag);
void	do_op_bench(t_stack *a, t_stack *b, t_bench *bench, char *op);
void	do_op_nobench(t_stack *a, t_stack *b, t_bench *bench, char *op);
/*---------------------------------parsing------------------------------------*/
char	*get_next_line(int fd);
int		ft_check_line(char *line);
char	*ft_strjoin(char *s1, char s2[]);
int		ft_check_flag(char **av, int ac);
char	**ft_split(char const *s, char c);
void	ft_format(char **line, char buffer[]);
int		parsing(t_stack *a, int ac, char **av);
void	choose_algo(t_stack *a, t_stack *b, int flag);

#endif
