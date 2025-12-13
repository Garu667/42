/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_checker.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 19:42:04 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/12 19:42:08 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

bool	is_sorted(t_stack *a)
{
	int	i;

	i = 0;
	while (i < (a->size - 1))
	{
		if (a->tab[i] > a->tab[i + 1])
			return (false);
		i++;
	}
	return (true);
}

static int	do_op(t_stack *a, t_stack *b, char *op)
{
	if (ft_strncmp(op, "sa\n", 3) == 0)
		sa(a, 0);
	else if (ft_strncmp(op, "sb\n", 3) == 0)
		sb(b, 0);
	else if (ft_strncmp(op, "ss\n", 3) == 0)
		ss(a, b, 0);
	else if (ft_strncmp(op, "pa\n", 3) == 0)
		pa(a, b, 0);
	else if (ft_strncmp(op, "pb\n", 3) == 0)
		pb(a, b, 0);
	else if (ft_strncmp(op, "ra\n", 3) == 0)
		ra(a, 0);
	else if (ft_strncmp(op, "rb\n", 3) == 0)
		rb(b, 0);
	else if (ft_strncmp(op, "rr\n", 3) == 0)
		rr(a, b, 0);
	else if (ft_strncmp(op, "rra\n", 4) == 0)
		rra(a, 0);
	else if (ft_strncmp(op, "rrb\n", 4) == 0)
		rrb(b, 0);
	else if (ft_strncmp(op, "rrr\n", 4) == 0)
		rrr(a, b, 0);
	else
		return (-1);
	return (0);
}

static int	checker(t_stack *a)
{
	char	*line;
	t_stack	b;

	b.size = 0;
	b.tab = malloc(a->size * sizeof(int));
	if (!b.tab)
		exit(write(2, "Error\n", 6));
	while (1)
	{
		line = get_next_line(0);
		if (!line)
			break ;
		if (do_op(a, &b, line) == -1)
			exit(write(2, "Error\n", 6));
		free(line);
	}
	if (is_sorted(a) && b.size == 0)
		ft_safe_write(1, "OK\n", 3);
	else
		ft_safe_write(1, "KO\n", 3);
	return (0);
}

int	main(int ac, char **av)
{
	t_stack	a;

	if (ac < 2)
		return (0);
	a = parsing(&ac, av, 1);
	checker(&a);
}
