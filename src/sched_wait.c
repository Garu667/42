/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sched_wait.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/15 10:00:00 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static long	next_wakeup(t_sim *sim)
{
	int		i;
	long	now;
	long	best;
	long	end;

	if (sim->qsize == 0)
		return (0);
	best = 0;
	now = get_time_ms();
	i = -1;
	while (++i < sim->n_coders)
	{
		pthread_mutex_lock(&sim->dongles[i].mutex);
		end = sim->dongles[i].released_at + sim->dongle_cd;
		if (!sim->dongles[i].in_use && end > now && (best == 0 || end < best))
			best = end;
		pthread_mutex_unlock(&sim->dongles[i].mutex);
	}
	return (best);
}

void	sched_wait(t_sim *sim)
{
	if (next_wakeup(sim) <= 0)
	{
		pthread_cond_wait(&sim->sched_cond, &sim->sched_mutex);
		return ;
	}
	pthread_mutex_unlock(&sim->sched_mutex);
	usleep(200);
	pthread_mutex_lock(&sim->sched_mutex);
}
