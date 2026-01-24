/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse_op.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/24 09:08:47 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

int	rra(t_stack *a, bool write_switch)
{
	if (!a || !a->head || !a->head->next)
		return (0);
	a->head = a->head->prev;
	if (write_switch)
		write(1, "rra\n", 4);
	return (1);
}

int	rrb(t_stack *b, bool write_switch)
{
	if (!b || !b->head || !b->head->next)
		return (0);
	b->head = b->head->prev;
	if (write_switch)
		write(1, "rrb\n", 4);
	return (1);
}

int	rrr(t_stack *a, t_stack *b, bool write_switch)
{
	if (!a || !a->head || !a->head->next
		|| !b || !b->head || !b->head->next)
		return (0);
	rra(a, false);
	rrb(b, false);
	if (write_switch)
		write(1, "rrr\n", 4);
	return (1);
}
