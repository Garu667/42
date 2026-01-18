/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/18 09:38:25 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static void	radix_pass(t_stack *a, t_stack *b, int bit_to_study, int size)
{
	int	i;

	i = 0;
	while (i < size)
	{
		if (((a->head->index >> bit_to_study) & 1) == 1)
			ra(a, true);
		else
			pb(b, a, true);
		i++;
	}
	while (b->size > 0)
		pa(a, b, true);
}

void	radix_sort(t_stack *a, t_stack *b)
{
	int	bit_to_study;
	int	max_bits;
	int	index_max;

	if (!a || is_sorted(a) || !b)
		return ;
	printf("\n\t -> Radix sort <- \n");
	index_max = (a->size) - 1;
	max_bits = 0;
	while (index_max >> max_bits)
		max_bits++;
	bit_to_study = 0;
	while (bit_to_study < max_bits)
	{
		radix_pass(a, b, bit_to_study, a->size);
		bit_to_study++;
	}
}
