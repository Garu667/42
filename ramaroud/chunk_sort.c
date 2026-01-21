/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 22:08:30 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

static int	find_max_one(t_stack *b)
{
	t_node	*current;
	int		max;
	int		i;

	i = 0;
	current = b->head;
	max = current->index;
	while (i < b->size)
	{
		if (current->index > max)
			max = current->index;
		current = current->next;
		i++;
	}
	return (max);
}

static void	chunk_pa(t_stack *a, t_stack *b, t_bench *bench)
{
	int	max;
	int	position;

	max = find_max_one(b);
	while (b->head->index != max)
	{
		position = get_position(b, max);
		if (position <= (b->size / 2))
			bench->op(a, b, bench, "rb\n");
		else
			bench->op(a, b, bench, "rrb\n");
	}
	bench->op(a, b, bench, "pa\n");
}

static void	chunk_pb(t_stack *a, t_stack *b, t_bench *bench, int min, int max)
{
	int	to_push;
	int	pushed;

	pushed = 0;
	to_push = max - min;
	while (pushed <= to_push)
	{
		if (a->head->index >= min && a->head->index <= max)
		{
			bench->op(a, b, bench, "pb\n");
			pushed++;
		}
		else
			bench->op(a, b, bench, "ra\n");
	}
}

static int	define_chunks_size(int size)
{
	if (size <= 10)
		return (3);
	return (5);
}

void	chunk_sort(t_stack *a, t_stack *b, t_bench *bench)
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
		chunk_pb(a, b, bench, min, max);
		min = min + chunks_size;
		max = max + chunks_size;
		if (max >= a->size + b->size)
			max = a->size + b->size - 1;
	}
	while (b->size > 0)
		chunk_pa(a, b, bench);
}
