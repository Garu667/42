/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 17:03:45 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	fill_waiter(t_coder *c)
{
	t_sim	*sim;

	sim = c->sim;
	pthread_mutex_lock(&sim->coders_mutex);
	c->waiter.coder_id = c->id;
	c->waiter.deadline = c->last_compile + sim->time_burnout;
	c->waiter.n_compile = c->compile_count;
	pthread_mutex_unlock(&sim->coders_mutex);
}

/*
** The coder never inspects a dongle. It registers a request, then sleeps on
** its own condvar until the arbiter has already flipped both dongles to
** in_use on its behalf. granted is the whole contract, and it is the loop
** predicate, so a spurious wakeup cannot make a coder leave empty-handed.
*/
int	request_dongles(t_coder *c)
{
	t_sim	*sim;
	int		ok;

	sim = c->sim;
	fill_waiter(c);
	pthread_mutex_lock(&sim->sched_mutex);
	c->waiter.seq = sim->seq++;
	c->granted = 0;
	queue_push(sim, &c->waiter);
	pthread_cond_signal(&sim->sched_cond);
	while (!c->granted && !sim_should_stop(sim))
		pthread_cond_wait(&c->cond, &sim->sched_mutex);
	ok = c->granted;
	if (!ok)
		queue_remove(sim, &c->waiter);
	pthread_mutex_unlock(&sim->sched_mutex);
	return (ok);
}

void	release_dongles(t_coder *c)
{
	t_sim	*sim;
	long	now;

	sim = c->sim;
	pthread_mutex_lock(&sim->sched_mutex);
	now = get_time_ms();
	c->left->in_use = 0;
	c->left->released_at = now;
	c->right->in_use = 0;
	c->right->released_at = now;
	c->granted = 0;
	pthread_cond_signal(&sim->sched_cond);
	pthread_mutex_unlock(&sim->sched_mutex);
}
