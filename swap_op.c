/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap_op.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:33:31 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:33:31 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	sa(t_stack *a, bool write_switch)
{
	t_node	*first;
	t_node	*second;
	t_node	*third;
	t_node	*last;

	if (!a || !a->head || a->head->next == a->head)
		return (0);
	first = a->head;
	second = first->next;
	third = second->next;
	last = first->prev;
	last->next = second;
	second->prev = last;
	a->head = second;
	second->next = first;
	first->prev = second;
	first->next = third;
	third->prev = first;
	if (write_switch)
		write(1, "sa\n", 3);
	return (1);
}

int	sb(t_stack *b, bool write_switch)
{
	t_node	*first;
	t_node	*second;
	t_node	*third;
	t_node	*last;

	if (!b || !b->head || b->head->next == b->head)
		return (0);
	first = b->head;
	second = first->next;
	third = second->next;
	last = first->prev;
	last->next = second;
	second->prev = last;
	b->head = second;
	second->next = first;
	first->prev = second;
	first->next = third;
	third->prev = first;
	if (write_switch)
		write(1, "sb\n", 3);
	return (1);
}

int	ss(t_stack *a, t_stack *b, bool write_switch)
{
	if (!a || !a->head || !a->head->next
		|| !b || !b->head || !b->head->next)
		return (0);
	sa(a, false);
	sb(b, false);
	if (write_switch)
		write(1, "ss\n", 3);
	return (1);
}
