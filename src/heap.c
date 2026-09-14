/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 11:14:17 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/14 11:14:17 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	has_priority(t_waiter *a, t_waiter *b, int scheduler)
{
	if (scheduler == SCHEDULER_FIFO)
	{
		if (a->arrived_at != b->arrived_at)
			return (a->arrived_at < b->arrived_at);
		return (a->coder_id < b->coder_id);
	}
	if (a->deadline != b->deadline)
		return (a->deadline < b->deadline);
	if (a->n_compile != b->n_compile)
		return (a->n_compile < b->n_compile);
	if (a->arrived_at != b->arrived_at)
		return (a->arrived_at < b->arrived_at);
	return (a->coder_id < b->coder_id);
}

t_waiter	*heap_peek(t_dongle *dongle)
{
	if (dongle->queue_size == 0)
		return (NULL);
	return (dongle->queue[0]);
}

void	heap_push(t_dongle *dongle, t_waiter *waiter, int scheduler)
{
	int	i;

	if (dongle->queue_size >= dongle->queue_cap)
		return ;
	i = dongle->queue_size;
	while (i > 0 && has_priority(waiter, dongle->queue[i - 1], scheduler))
	{
		dongle->queue[i] = dongle->queue[i - 1];
		i--;
	}
	dongle->queue[i] = waiter;
	dongle->queue_size++;
}

void	heap_remove(t_dongle *dongle, t_waiter *waiter)
{
	int	i;

	i = 0;
	while (i < dongle->queue_size && dongle->queue[i] != waiter)
		i++;
	if (i == dongle->queue_size)
		return ;
	dongle->queue_size--;
	while (i < dongle->queue_size)
	{
		dongle->queue[i] = dongle->queue[i + 1];
		i++;
	}
}
