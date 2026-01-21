/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 11:13:20 by quentin          ###   ########.fr       */
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

static void	chunk_pb(t_stack *a, t_stack *b,
	t_bench *bench, int min)
{
	int	chunk_size;
	int	max;
	int	rotations;
	int	targets;

	chunk_size = define_chunks_size(a->size + b->size);
	max = min + chunk_size - 1;
	if (max >= a->size + b->size)
		max = a->size + b->size - 1;

	targets = max - min + 1;
	rotations = 0;
	while (rotations < a->size && targets > 0)
	{
		if (a->head->index >= min && a->head->index <= max)
		{
			bench->op(a, b, bench, "pb\n");
			targets--;
		}
		else
			bench->op(a, b, bench, "ra\n");
		rotations++;
	}
}


void	chunk_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	int	min;
	int	chunk_size;

	if (!a || !b || is_sorted(a))
		return ;
	bench->strats |= FLAG_MEDIUM;
	printf("\n\t -> Chunk sort <- \n");
	chunk_size = define_chunks_size(a->size);
	min = 0;
	while (a->size > 0)
	{
		chunk_pb(a, b, bench, min);
		min += chunk_size;
	}
	while (b->size > 0)
		chunk_pa(a, b, bench);
}
