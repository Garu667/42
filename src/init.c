/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 16:06:15 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	init_dongles(t_sim *sim)
{
	int	i;

	i = -1;
	while (++i < sim->n_coders)
	{
		pthread_mutex_init(&sim->dongles[i].mutex, NULL);
		sim->dongles[i].in_use = 0;
		sim->dongles[i].reserved = 0;
		sim->dongles[i].released_at = 0;
	}
}

static void	init_coders(t_sim *sim)
{
	int	i;

	i = -1;
	while (++i < sim->n_coders)
	{
		sim->coders[i].id = i + 1;
		sim->coders[i].sim = sim;
		sim->coders[i].left = &sim->dongles[i];
		sim->coders[i].right = &sim->dongles[(i + 1) % sim->n_coders];
		sim->coders[i].last_compile = sim->sim_start;
		sim->coders[i].compile_count = 0;
		sim->coders[i].granted = 0;
		pthread_cond_init(&sim->coders[i].cond, NULL);
	}
}

static void	init_unbreakable(t_sim *sim)
{
	sim->qsize = 0;
	sim->seq = 0;
	init_dongles(sim);
	pthread_mutex_init(&sim->sched_mutex, NULL);
	pthread_cond_init(&sim->sched_cond, NULL);
	pthread_mutex_init(&sim->stop_mutex, NULL);
	pthread_mutex_init(&sim->log_mutex, NULL);
	pthread_mutex_init(&sim->coders_mutex, NULL);
	sim->sim_start = get_time_ms();
	init_coders(sim);
}

static int	start_coders(t_sim *sim)
{
	int	i;

	i = -1;
	while (++i < sim->n_coders)
	{
		if (pthread_create(&sim->coders[i].thread, NULL,
				coder_routine, &sim->coders[i]) != 0)
			return (free_return(sim, 4, ERR_THREAD_CREATE, i));
	}
	start_simulation(sim);
	pthread_join(sim->monitor, NULL);
	pthread_join(sim->arbiter, NULL);
	return (0);
}

int	init_sim(t_sim *sim)
{
	sim->coders = malloc(sim->n_coders * sizeof(t_coder));
	if (!sim->coders)
		return (free_return(sim, 0, ERR_ALLOC_CODERS, 0));
	sim->dongles = malloc(sim->n_coders * sizeof(t_dongle));
	if (!sim->dongles)
		return (free_return(sim, 1, ERR_ALLOC_DONGLES, 0));
	sim->queue = malloc(sim->n_coders * sizeof(t_waiter *));
	if (!sim->queue)
		return (free_return(sim, 2, ERR_ALLOC_QUEUE, 0));
	init_unbreakable(sim);
	if (pthread_create(&sim->arbiter, NULL, sched_routine, sim))
		return (free_return(sim, 3, ERR_THREAD_CREATE, 0));
	if (pthread_create(&sim->monitor, NULL, monitor_routine, sim))
		return (free_return(sim, 5, ERR_THREAD_CREATE, 0));
	return (start_coders(sim));
}
