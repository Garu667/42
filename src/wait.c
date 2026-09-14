/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   wait.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/12 10:00:00 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/12 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static long	cooldown_end(t_dongle *d, long cd)
{
	if (d->in_use)
		return (0);
	if (get_time_ms() - d->released_at >= cd)
		return (0);
	return (d->released_at + cd);
}

static long	next_wakeup(t_coder *c)
{
	long	a;
	long	b;

	pthread_mutex_lock(&c->left->mutex);
	a = cooldown_end(c->left, c->sim->dongle_cd);
	pthread_mutex_unlock(&c->left->mutex);
	pthread_mutex_lock(&c->right->mutex);
	b = cooldown_end(c->right, c->sim->dongle_cd);
	pthread_mutex_unlock(&c->right->mutex);
	if (b > a)
		return (b);
	return (a);
}

void	wait_table(t_coder *c)
{
	struct timespec	ts;
	long			target;

	target = next_wakeup(c);
	if (target > 0)
	{
		ts.tv_sec = target / 1000;
		ts.tv_nsec = (target % 1000) * 1000000L;
		if (ts.tv_nsec >= 1000000000L)
		{
			ts.tv_sec += 1;
			ts.tv_nsec -= 1000000000L;
		}
		pthread_cond_timedwait(&c->sim->table_cond, &c->sim->table_mutex, &ts);
	}
	else
		pthread_cond_wait(&c->sim->table_cond, &c->sim->table_mutex);
}

void	acquire_pair(t_coder *c)
{
	t_sim	*sim;

	sim = c->sim;
	pthread_mutex_lock(&sim->coders_mutex);
	c->waiter.coder_id = c->id;
	c->waiter.arrived_at = get_time_ms();
	c->waiter.deadline = c->last_compile + sim->time_burnout;
	c->waiter.n_compile = c->compile_count;
	pthread_mutex_unlock(&sim->coders_mutex);
	pthread_mutex_lock(&sim->table_mutex);
	queue_pair(c, 1);
	while (!sim_should_stop(sim) && !try_claim(c))
		wait_table(c);
	if (sim_should_stop(sim))
		queue_pair(c, 0);
	pthread_cond_broadcast(&sim->table_cond);
	pthread_mutex_unlock(&sim->table_mutex);
}
