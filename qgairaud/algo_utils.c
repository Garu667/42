/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   algo_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/17 22:20:02 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

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
void	push_min(t_stack *a, t_stack *b)
{
	int	position;

	position = get_position(a, 0);
	if (position <= a->size / 2)
	{
		while (position--)
			ra(a, true);
	}
	else
	{
		while (position++ < a->size)
			rra(a, true);
	}
	pb(b, a, true);
}