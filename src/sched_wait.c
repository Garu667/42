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

/*
** Earliest instant at which the state can change on its own, i.e. the soonest
** cooldown expiry. A dongle that is in_use contributes nothing: its release
** will signal us. Returning 0 means "wait until somebody wakes us".
*/
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
		end = sim->dongles[i].released_at + sim->dongle_cd;
		if (!sim->dongles[i].in_use && end > now && (best == 0 || end < best))
			best = end;
	}
	return (best);
}

/*
** No timed wait: cond_wait whenever the only thing that can unblock us is
** another thread (a release or a new request). During a cooldown nothing will
** signal us, so we drop the mutex for a short sleep instead. Missing a signal
** in that window is harmless: we rescan as soon as we take the mutex back.
*/
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
