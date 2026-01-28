/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_op.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/28 17:46:20 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static t_node	*extract_head(t_stack *stack)
{
	t_node	*node;

	if (!stack || !stack->head)
		return (NULL);
	node = stack->head;
	if (node->next == node)
		stack->head = NULL;
	else
	{
		node->prev->next = node->next;
		node->next->prev = node->prev;
		stack->head = node->next;
	}
	stack->size--;
	return (node);
}

static void	insert_head(t_stack *stack, t_node *node)
{
	if (!stack || !node)
		return ;
	if (!stack->head)
	{
		node->next = node;
		node->prev = node;
		stack->head = node;
	}
	else
	{
		node->next = stack->head;
		node->prev = stack->head->prev;
		stack->head->prev->next = node;
		stack->head->prev = node;
		stack->head = node;
	}
	stack->size++;
}

int	pa(t_stack *a, t_stack *b, bool write_switch)
{
	t_node	*node;

	if (!a || !b)
		return (0);
	node = extract_head(b);
	if (!node)
		return (0);
	insert_head(a, node);
	if (write_switch)
		write(1, "pa\n", 3);
	return (1);
}

int	pb(t_stack *a, t_stack *b, bool write_switch)
{
	t_node	*node;

	if (!a || !b)
		return (0);
	node = extract_head(a);
	if (!node)
		return (0);
	insert_head(b, node);
	if (write_switch)
		write(1, "pb\n", 3);
	return (1);
}
