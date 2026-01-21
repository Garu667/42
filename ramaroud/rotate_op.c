/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate_operations.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/17 21:51:20 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

int	ra(t_stack *a, bool write_switch)
{
	if (!a || !a->head || !a->head->next)
		return (0);
	a->head = a->head->next;
	if (write_switch)
		write(1, "ra\n", 3);
	return (1);
}

int	rb(t_stack *b, bool write_switch)
{
	if (!b || !b->head || !b->head->next)
		return (0);
	b->head = b->head->next;
	if (write_switch)
		write(1, "rb\n", 3);
	return (1);
}

int	rr(t_stack *a, t_stack *b, bool write_switch)
{
	if (!a || !a->head || !a->head->next
		|| !b || !b->head || !b->head->next)
		return (0);
	ra(a, false);
	rb(b, false);
	if (write_switch)
		write(1, "rr\n", 3);
	return (1);
}
