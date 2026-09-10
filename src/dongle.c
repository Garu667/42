/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 17:03:45 by ramaroud          #+#    #+#             */
/*   Updated: 2026/07/27 17:03:45 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

/*
static int	dongle_ready(t_dongle *dongle, t_waiter *waiter, long dongle_cd)
{
	if (dongle->in_use)
		return (0);
	if (get_time_ms() - dongle->released_at < dongle_cd)
		return (0);
	return (heap_peek(dongle) == waiter);
}

void	acquire_dongle(t_coder *coder, t_dongle *dongle)
{
	t_waiter	waiter;

	waiter.coder_id = coder->id;
	waiter.arrived_at = get_time_ms();
	waiter.deadline = coder->last_compile + coder->sim->time_burnout;
	pthread_mutex_lock(&dongle->mutex);
	heap_push(dongle, &waiter, coder->sim->scheduler);
	while (!dongle_ready(dongle, &waiter, coder->sim->dongle_cd)
		&& !sim_should_stop(coder->sim))
	{
		pthread_mutex_unlock(&dongle->mutex);
		usleep(500);
		pthread_mutex_lock(&dongle->mutex);
	}
	if (dongle_ready(dongle, &waiter, coder->sim->dongle_cd)
		&& !sim_should_stop(coder->sim))
	{
		dongle->in_use = 1;
		heap_pop(dongle);
	}
	else if (dongle->queue_size == 2)
		dongle->queue_size--;
	pthread_mutex_unlock(&dongle->mutex);
}
*/

void	release_dongle(t_dongle *dongle)
{
	pthread_mutex_lock(&dongle->mutex);
	dongle->in_use = 0;
	dongle->released_at = get_time_ms();
	pthread_mutex_unlock(&dongle->mutex);
}

static int	dongle_ready(t_dongle *dongle, long dongle_cd)
{
	if (dongle->in_use)
		return (0);
	if (get_time_ms() - dongle->released_at < dongle_cd)
		return (0);
	return (1);
}

static int	is_my_turn(t_dongle *dongle, t_coder *coder)
{
	t_waiter	*waiter;

	waiter = heap_peek(dongle);
	if (!waiter)
		return (1);
	return (waiter->coder_id == coder->id);
}

void	register_waiter(t_dongle *first, t_dongle *second, t_coder *coder)
{
	t_waiter	*waiter;

	waiter = &coder->waiter;
	waiter->coder_id = coder->id;
	waiter->arrived_at = get_time_ms();
	waiter->deadline = coder->last_compile + coder->sim->time_burnout;
	pthread_mutex_lock(&first->mutex);
	pthread_mutex_lock(&second->mutex);
	heap_push(first, waiter, coder->sim->scheduler);
	heap_push(second, waiter, coder->sim->scheduler);
	pthread_mutex_unlock(&second->mutex);
	pthread_mutex_unlock(&first->mutex);
}

int	acquire_dongles(t_coder *coder, t_dongle *first, t_dongle *second)
{
	t_sim	*sim;

	sim = coder->sim;
	register_waiter(first, second, coder);
	while (!sim_should_stop(sim))
	{
		pthread_mutex_lock(&first->mutex);
		pthread_mutex_lock(&second->mutex);
		if (dongle_ready(first, sim->dongle_cd)
			&& dongle_ready(second, sim->dongle_cd)
			&& is_my_turn(first, coder)
			&& is_my_turn(second, coder))
		{
			first->in_use = 1;
			second->in_use = 1;
			heap_pop(first);
			heap_pop(second);
			pthread_mutex_unlock(&second->mutex);
			pthread_mutex_unlock(&first->mutex);
			return (1);
		}
		pthread_mutex_unlock(&second->mutex);
		pthread_mutex_unlock(&first->mutex);
		usleep(500);
	}
	return (0);
}
