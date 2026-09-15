/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/15 10:00:00 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	dongle_free(t_sim *sim, t_dongle *d, long now)
{
	if (d->in_use || d->reserved)
		return (0);
	return (now - d->released_at >= sim->dongle_cd);
}

/*
** Either hand both dongles to this waiter, or reserve both for it so that no
** lower-priority waiter can take them later in this same pass. That reservation
** is the whole anti-starvation argument: a blocked waiter is only ever blocked
** by coders that are compiling, and they release after time_compile.
*/
static int	try_grant(t_sim *sim, t_waiter *w, long now)
{
	t_coder	*c;

	c = &sim->coders[w->coder_id - 1];
	if (!dongle_free(sim, c->left, now) || !dongle_free(sim, c->right, now))
	{
		c->left->reserved = 1;
		c->right->reserved = 1;
		return (0);
	}
	c->left->in_use = 1;
	c->right->in_use = 1;
	queue_remove(sim, w);
	c->granted = 1;
	pthread_cond_signal(&c->cond);
	return (1);
}

static void	sched_scan(t_sim *sim)
{
	int		i;
	long	now;

	i = -1;
	now = get_time_ms();
	while (++i < sim->n_coders)
		sim->dongles[i].reserved = 0;
	i = 0;
	while (i < sim->qsize)
	{
		if (!try_grant(sim, sim->queue[i], now))
			i++;
	}
}

void	*sched_routine(void *arg)
{
	t_sim	*sim;

	sim = (t_sim *)arg;
	pthread_mutex_lock(&sim->sched_mutex);
	while (!sim_should_stop(sim))
	{
		sched_scan(sim);
		if (sim_should_stop(sim))
			break ;
		sched_wait(sim);
	}
	pthread_mutex_unlock(&sim->sched_mutex);
	return (NULL);
}
