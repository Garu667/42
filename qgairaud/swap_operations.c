/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap_operations.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 14:16:44 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	sa(t_stack *a, bool write_switch)
{
	t_node	*first;
	t_node	*second;

	if (!a || !a->head || !a->head->next)
		return (0);
	first = a->head;
	second = first->next;
	first->next = second->next;
	a->head = second;
	second->next = first;
	if (write_switch)
		write(1, "sa\n", 3);
	return (1);
}

int	sb(t_stack *b, bool write_switch)
{
	t_node	*first;
	t_node	*second;

	if (!b || !b->head || !b->head->next)
		return (0);
	first = b->head;
	second = first->next;
	first->next = second->next;
	b->head = second;
	second->next = first;
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
