/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 21:36:21 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static int	define_chunks_size(int size)
{
	if (size <= 100)
		return (size / 5);
	return (size / 10);
}

static int	find_max_one(t_stack *b)
{
	t_node	*current;
	int		max;

	current = b->head;
	max = current->index;
	while (current)
	{
		if (current->index > max)
			max = current->index;
		current = current->next;
	}
	return (max);
}

static void	chunk_pa(t_stack *a, t_stack *b, t_bench *bench)
{
	int	max;
	int	position;

	max = find_max_one(b);
	position = get_position(b, max);
	while (b->head->index != max)
	{
		if (position <= b->size / 2)
			bench->op(a, b, bench, "rb\n");
		else
			bench->op(a, b, bench, "rrb\n");
	}
	bench->op(a, b, bench, "pa\n");
}

static void	chunk_pb(t_stack *a, t_stack *b, t_bench *bench, int min)
{
	int	max;
	int	to_push;
	int	pushed;

	max = min + define_chunks_size(a->size + b->size) - 1;
	if (max >= a->size + b->size)
		max = a->size + b->size - 1;
	to_push = max - min + 1;
	pushed = 0;
	while (pushed < to_push)
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

void	chunk_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	int	min;
	int	total;
	int	chunk_size;

	if (!a || !b || is_sorted(a))
		return ;
	printf("\n\t -> Chunk sort <- \n");
	total = a->size;
	chunk_size = define_chunks_size(total);
	min = 0;
	while (a->size > 0)
	{
		chunk_pb(a, b, bench, min);
		min += chunk_size;
	}
	while (b->size > 0)
		chunk_pa(a, b, bench);
}