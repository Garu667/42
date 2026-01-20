/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 14:15:58 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static int	define_chunks_size(int size)
{
	if (size <= 100)
		return (size / 5);
	return (size / 10);
}

void	chunk_sort(t_stack *a, t_stack *b)
{
	int	chunks_size;
	int	min;
	int	max;

	if (!a || is_sorted(a) || !b)
		return ;
	printf("\n\t -> Chunk sort <- \n");
	chunks_size = define_chunks_size(a->size);
	min = 0;
	max = chunks_size - 1;
	while (a->size > 0)
	{
		chunk_pb(a, b, min, max);
		min = min + chunks_size;
		max = max + chunks_size;
		if (max >= a->size + b->size)
			max = a->size + b->size - 1;
	}
	while (b->size > 0)
		chunk_pa(a, b);
}
