/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_op.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 09:12:56 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

int pa(t_stack *a, t_stack *b, bool write_switch)
{
	t_node *node;
	t_node *a_last;
	t_node *b_last;

	if (!a || !b || !b->head)
		return (0);
	node = b->head;
	if (b->head->next == b->head)
		b->head = NULL;
	else
	{
		b_last = b->head->prev;
		b->head = b->head->next;
		b->head->prev = b_last;
		b_last->next = b->head;
	}
	b->size--;
	if (!a->head)
	{
		node->next = node;
		node->prev = node;
		a->head = node;
	}
	else
	{
		a_last = a->head->prev;
		node->next = a->head;
		node->prev = a_last;
		a_last->next = node;
		a->head->prev = node;
		a->head = node;
	}
	a->size++;
	if (write_switch)
		write(1, "pa\n", 3);
	return (1);
}

int pb(t_stack *a, t_stack *b, bool write_switch)
{
	t_node *node;
	t_node *a_last;
	t_node *b_last;

	if (!a || !b || !a->head)
		return (0);
	node = a->head;
	if (a->head->next == a->head)
		a->head = NULL;
	else
	{
		a_last = a->head->prev;
		a->head = a->head->next;
		a->head->prev = a_last;
		a_last->next = a->head;
	}
	a->size--;
	if (!b->head)
	{
		node->next = node;
		node->prev = node;
		b->head = node;
	}
	else
	{
		b_last = b->head->prev;
		node->next = b->head;
		node->prev = b_last;
		b_last->next = node;
		b->head->prev = node;
		b->head = node;
	}
	b->size++;
	if (write_switch)
		write(1, "pb\n", 3);
	return (1);
}
