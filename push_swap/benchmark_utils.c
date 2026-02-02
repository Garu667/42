/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   benchmark_utils.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:31:44 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:31:44 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	do_op_bench(t_stack *a, t_stack *b, t_bench *bench, char *op)
{
	if (ft_strncmp(op, "sa\n", 3) == 0)
		bench->ops[0] += sa(a, 1);
	else if (ft_strncmp(op, "sb\n", 3) == 0)
		bench->ops[1] += sb(b, 1);
	else if (ft_strncmp(op, "ss\n", 3) == 0)
		bench->ops[2] += ss(a, b, 1);
	else if (ft_strncmp(op, "pa\n", 3) == 0)
		bench->ops[3] += pa(a, b, 1);
	else if (ft_strncmp(op, "pb\n", 3) == 0)
		bench->ops[4] += pb(a, b, 1);
	else if (ft_strncmp(op, "ra\n", 3) == 0)
		bench->ops[5] += ra(a, 1);
	else if (ft_strncmp(op, "rb\n", 3) == 0)
		bench->ops[6] += rb(b, 1);
	else if (ft_strncmp(op, "rr\n", 3) == 0)
		bench->ops[7] += rr(a, b, 1);
	else if (ft_strncmp(op, "rra\n", 4) == 0)
		bench->ops[8] += rra(a, 1);
	else if (ft_strncmp(op, "rrb\n", 4) == 0)
		bench->ops[9] += rrb(b, 1);
	else if (ft_strncmp(op, "rrr\n", 4) == 0)
		bench->ops[10] += rrr(a, b, 1);
}

void	do_op_nobench(t_stack *a, t_stack *b, t_bench *bench, char *op)
{
	(void)bench;
	if (ft_strncmp(op, "sa\n", 3) == 0)
		sa(a, 1);
	else if (ft_strncmp(op, "sb\n", 3) == 0)
		sb(b, 1);
	else if (ft_strncmp(op, "ss\n", 3) == 0)
		ss(a, b, 1);
	else if (ft_strncmp(op, "pa\n", 3) == 0)
		pa(a, b, 1);
	else if (ft_strncmp(op, "pb\n", 3) == 0)
		pb(a, b, 1);
	else if (ft_strncmp(op, "ra\n", 3) == 0)
		ra(a, 1);
	else if (ft_strncmp(op, "rb\n", 3) == 0)
		rb(b, 1);
	else if (ft_strncmp(op, "rr\n", 3) == 0)
		rr(a, b, 1);
	else if (ft_strncmp(op, "rra\n", 4) == 0)
		rra(a, 1);
	else if (ft_strncmp(op, "rrb\n", 4) == 0)
		rrb(b, 1);
	else if (ft_strncmp(op, "rrr\n", 4) == 0)
		rrr(a, b, 1);
}
