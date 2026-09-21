/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 15:07:49 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 19:04:00 by ramaroud         ###   ########lyon.fr   */
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

static void	sift_up(t_sim *sim, int index)
{
	int	parent;

	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (!has_priority(sim->queue[index],
				sim->queue[parent], sim->scheduler))
			break ;
		swap_waiters(&sim->queue[index], &sim->queue[parent]);
		index = parent;
	}
}

static void	sift_down(t_sim *sim, int index)
{
	int	left;
	int	right;
	int	best;

	while (1)
	{
		left = index * 2 + 1;
		right = index * 2 + 2;
		best = index;
		if (left < sim->qsize
			&& has_priority(sim->queue[left],
				sim->queue[best], sim->scheduler))
			best = left;
		if (right < sim->qsize
			&& has_priority(sim->queue[right],
				sim->queue[best], sim->scheduler))
			best = right;
		if (best == index)
			break ;
		swap_waiters(&sim->queue[index], &sim->queue[best]);
		index = best;
	}
}

void	heap_push(t_sim *sim, t_waiter *waiter)
{
	if (sim->qsize >= sim->n_coders)
		return ;
	sim->queue[sim->qsize] = waiter;
	sim->qsize++;
	sift_up(sim, sim->qsize - 1);
}

void	heap_remove(t_sim *sim, t_waiter *waiter)
{
	int	i;

	i = 0;
	while (i < sim->qsize && sim->queue[i] != waiter)
		i++;
	if (i == sim->qsize)
		return ;
	sim->qsize--;
	if (i == sim->qsize)
		return ;
	sim->queue[i] = sim->queue[sim->qsize];
	if (i > 0
		&& has_priority(sim->queue[i],
			sim->queue[(i - 1) / 2], sim->scheduler))
		sift_up(sim, i);
	else
		sift_down(sim, i);
}
