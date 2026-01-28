/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/24 09:06:52 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

static int	define_chunks_size(int size)
{
	int		x;

	x = 1;
	while ((x * x) < size)
		x++;
	return (x);
}

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

static void	chunk_pb(t_stack *a, t_stack *b, t_bench *bench, t_chunk *chunk)
{
	int	to_push;
	int	pushed;

	to_push = chunk->max - chunk->min;
	pushed = 0;
	while (pushed <= to_push)
	{
		if (a->head->index >= chunk->min && a->head->index <= chunk->max)
		{
			bench->op(a, b, bench, "pb\n");
			pushed++;
		}
		else
			bench->op(a, b, bench, "ra\n");
	}
}

void	chunk_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	int			chunks_size;
	t_chunk		chunk;

	if (!a || is_sorted(a) || !b)
		return ;
	chunks_size = define_chunks_size(a->size);
	chunk.max = chunks_size - 1;
	chunk.min = 0;
	while (a->size > 0)
	{
		chunk_pb(a, b, bench, &chunk);
		chunk.min = chunk.min + chunks_size;
		chunk.max = chunk.max + chunks_size;
		if (chunk.max >= a->size + b->size)
			chunk.max = a->size + b->size - 1;
	}
	while (b->size > 0)
		chunk_pa(a, b, bench);
}
