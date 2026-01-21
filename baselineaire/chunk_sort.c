/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 10:29:20 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

static int	define_chunks_size(int size)
{
	if (size <= 5)
		return (1);
	else if (size <= 100)
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
		if (position <= (b->size / 2))
			bench->op(a, b, bench, "rb\n");
		else
			bench->op(a, b, bench, "rrb\n");
	}
	bench->op(a, b, bench, "pa\n");
}

static void	chunk_pb(t_stack *a, t_stack *b, t_bench *bench, int max)
{
	int	min;
	int	rotations;
	int	limit;
	int	chunk_size;
	
	chunk_size = define_chunks_size(a->size + b->size);
	min = (max / chunk_size) * chunk_size;
	rotations = 0;
	limit = a->size;
	while (rotations < limit)
	{
		if (a->head->index >= min && a->head->index <= max)
		{
			bench->op(a, b, bench, "pb\n");
			rotations = 0;
			limit = a->size;	
		}
		else
		{
			bench->op(a, b, bench, "ra\n");
			rotations++;
		}
	}
}

void	chunk_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	int	min;
	int	max;
	int	total;
	int	chunks_size;

	if (!a || is_sorted(a) || !b)
		return ;
	total = a->size;
	chunks_size = define_chunks_size(total);
	min = 0;
	max = chunks_size - 1;
	while (a->size > 0)
	{
		chunk_pb(a, b, bench, max);
		min = min + chunks_size;
		max = max + chunks_size;
		if (max >= a->size + b->size)
			max = a->size + b->size - 1;
	}
	while (b->size > 0)
		chunk_pa(a, b, bench);
}
