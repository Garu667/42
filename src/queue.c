/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/15 10:00:00 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	has_priority(t_waiter *a, t_waiter *b, int scheduler)
{
	if (scheduler == SCHEDULER_FIFO)
		return (a->seq < b->seq);
	if (a->deadline != b->deadline)
		return (a->deadline < b->deadline);
	if (a->n_compile != b->n_compile)
		return (a->n_compile < b->n_compile);
	return (a->seq < b->seq);
}

void	queue_push(t_sim *sim, t_waiter *waiter)
{
	int	i;

	if (sim->qsize >= sim->n_coders)
		return ;
	i = sim->qsize;
	while (i > 0 && has_priority(waiter, sim->queue[i - 1], sim->scheduler))
	{
		sim->queue[i] = sim->queue[i - 1];
		i--;
	}
	sim->queue[i] = waiter;
	sim->qsize++;
}

void	queue_remove(t_sim *sim, t_waiter *waiter)
{
	int	i;

	i = 0;
	while (i < sim->qsize && sim->queue[i] != waiter)
		i++;
	if (i == sim->qsize)
		return ;
	sim->qsize--;
	while (i < sim->qsize)
	{
		sim->queue[i] = sim->queue[i + 1];
		i++;
	}
}
