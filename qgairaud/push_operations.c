/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_operations.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 14:16:29 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	pa(t_stack *a, t_stack *b, bool write_switch)
{
	t_node	*tmp;

	if (!b || !b->head || !a)
		return (0);
	tmp = b->head;
	b->head = b->head->next;
	tmp->next = a->head;
	a->head = tmp;
	a->size++;
	b->size--;
	if (write_switch)
		write(1, "pa\n", 3);
	return (1);
}

int	pb(t_stack *b, t_stack *a, bool write_switch)
{
	t_node	*tmp;

	if (!a || !a->head || !b)
		return (0);
	tmp = a->head;
	a->head = a->head->next;
	tmp->next = b->head;
	b->head = tmp;
	b->size++;
	a->size--;
	if (write_switch)
		write(1, "pb\n", 3);
	return (1);
}
