/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   algo_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 09:08:50 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

int	get_position(t_stack *stack, int index)
{
	int		position;
	t_node	*current;

	current = stack->head;
	position = 0;
	while (current)
	{
		if (current->index == index)
			return (position);
		current = current->next;
		position++;
	}
	return (-1);
}

int	find_min_position(t_stack *a)
{
	t_node	*current;
	int		i;
	int		min_value;
	int		position;

	current = a->head;
	min_value = current->value;
	position = 0;
	i = 0;
	while (current)
	{
		if (current->value < min_value)
		{
			min_value = current->value;
			position = i;
		}
		current = current->next;
		i++;
	}
	return (position);
}

void	bring_min_top(t_stack *a, t_stack *b, t_bench *bench)
{
	int	position;

	position = find_min_position(a);
	if (position <= a->size / 2)
	{
		while (position > 0)
		{
			bench->op(a, b, bench, "ra\n");
			position--;
		}
	}
	else
	{
		while (position < a->size)
		{
			bench->op(a, b, bench, "rra\n");
			position++;
		}
	}
}
