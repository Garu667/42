/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   algo.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 07:12:36 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/13 07:12:37 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static int	min_index(t_stack *a)
{
	int	min;
	int	i;
	int	j;

	i = 1;
	j = 0;
	min = a->tab[0];
	while (i < a->size)
	{
		if (a->tab[i] < min)
		{
			min = a->tab[i];
			j = i;
		}
		i++;
	}
	return (j);
}

void	select_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	int	index;

	bench->strats |= FLAG_SIMPLE;
	if (is_sorted(a))
		return ;
	while (a->size)
	{
		index = min_index(a);
		if (index <= (a->size / 2))
		{
			while (index-- > 0)
				bench->op(a, b, bench, "ra\n");
		}
		else
		{
			index = a->size - index;
			while (index-- > 0)
				bench->op(a, b, bench, "rra\n");
		}
		bench->op(a, b, bench, "pb\n");
	}
	while (b->size)
		bench->op(a, b, bench, "pa\n");
}
