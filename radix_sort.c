/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:33:05 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:33:05 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static void	radix_pass(t_stack *a, t_stack *b, int bit_to_study, t_bench *bench)
{
	int	i;
	int	size;

	i = 0;
	size = a->size;
	while (i < size)
	{
		if (((a->head->index >> bit_to_study) & 1) == 1)
			bench->op(a, b, bench, "ra\n");
		else
			bench->op(a, b, bench, "pb\n");
		i++;
	}
	while (b->size > 0)
		bench->op(a, b, bench, "pa\n");
}

void	radix_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	int	bit_to_study;
	int	max_bits;
	int	index_max;

	if (!a || is_sorted(a) || !b)
		return ;
	index_max = (a->size) - 1;
	max_bits = 0;
	while (index_max >> max_bits)
		max_bits++;
	bit_to_study = 0;
	while (bit_to_study < max_bits)
	{
		radix_pass(a, b, bit_to_study, bench);
		bit_to_study++;
	}
}
