/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   algo_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:31:30 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:31:30 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	get_position(t_stack *stack, int index)
{
	t_node	*current;
	int		pos;
	int		i;

	i = 0;
	pos = 0;
	current = stack->head;
	while (i < stack->size)
	{
		if (current->index == index)
			return (pos);
		current = current->next;
		pos++;
		i++;
	}
	return (-1);
}

int	find_min_position(t_stack *a)
{
	t_node	*current;
	int		min;
	int		pos;
	int		i;

	i = 0;
	pos = 0;
	current = a->head;
	min = current->value;
	while (i < a->size)
	{
		if (current->value < min)
		{
			min = current->value;
			pos = i;
		}
		current = current->next;
		i++;
	}
	return (pos);
}

void	bring_min_top(t_stack *a, t_stack *b, t_bench *bench)
{
	int	pos;

	pos = find_min_position(a);
	if (pos <= (a->size / 2))
	{
		while (pos-- > 0)
			bench->op(a, b, bench, "ra\n");
	}
	else
	{
		pos = a->size - pos;
		while (pos-- > 0)
			bench->op(a, b, bench, "rra\n");
	}
}

bool	is_sorted(t_stack *a)
{
	t_node	*current;
	int		i;

	if (!a || !a->head || a->size <= 1)
		return (true);
	current = a->head;
	i = 0;
	while (i < (a->size - 1))
	{
		if (current->value > current->next->value)
			return (false);
		current = current->next;
		i++;
	}
	return (true);
}
