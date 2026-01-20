/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   chunk_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 14:16:01 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static int	is_in_chunk(int index, int min, int max)
{
	if (index >= min && index <= max)
		return (1);
	return (0);
}

void	chunk_pb(t_stack *a, t_stack *b, int min, int max)
{
	int	to_push;
	int	pushed;

	to_push = max - min;
	pushed = 0;
	while (pushed <= to_push)
	{
		if (is_in_chunk(a->head->index, min, max))
		{
			pb(b, a, true);
			pushed++;
		}
		else
			ra(a, true);
	}
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

void	chunk_pa(t_stack *a, t_stack *b)
{
	int	max;
	int	position;

	max = find_max_one(b);
	position = get_position(b, max);
	while (b->head->index != max)
	{
		if (position <= b->size / 2)
			rb(b, true);
		else
			rrb(b, true);
	}
	pa(a, b, true);
}
