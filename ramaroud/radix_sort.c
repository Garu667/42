/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 19:45:19 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

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
