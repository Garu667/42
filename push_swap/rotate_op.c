/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate_op.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:33:17 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:33:17 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

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
	ra(a, false);
	rb(b, false);
	if (write_switch)
		write(1, "rr\n", 3);
	return (1);
}
