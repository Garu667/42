/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 14:18:32 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 19:04:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*stop_simulation(t_sim *sim)
{
	int	i;

	pthread_mutex_lock(&sim->stop_mutex);
	sim->stop = 1;
	pthread_mutex_unlock(&sim->stop_mutex);
	pthread_mutex_lock(&sim->sched_mutex);
	i = -1;
	while (++i < sim->n_coders)
		pthread_cond_broadcast(&sim->coders[i].cond);
	pthread_cond_broadcast(&sim->sched_cond);
	pthread_mutex_unlock(&sim->sched_mutex);
	return (NULL);
}

void	*monitor_routine(void *arg)
{
	t_sim	*sim;
	long	time;
	int		done;
	int		i;

	sim = (t_sim *)arg;
	wait_for_start(sim);
	while (!sim_should_stop(sim))
	{
		i = -1;
		usleep(100);
		while (++i < sim->n_coders)
		{
			time = coder_status(sim, i, &done);
			if (!done && time >= sim->time_burnout)
			{
				log_action(sim, sim->coders[i].id, "burned out");
				return (stop_simulation(sim));
			}
		}
		if (all_coders_done(sim))
			stop_simulation(sim);
	}
	return (NULL);
}

void	wait_for_start(t_sim *sim)
{
	int	go;

	go = 0;
	while (!go)
	{
		pthread_mutex_lock(&sim->stop_mutex);
		go = (sim->can_start || sim->stop);
		pthread_mutex_unlock(&sim->stop_mutex);
		if (!go)
			usleep(100);
	}
}

void	start_simulation(t_sim *sim)
{
	int	i;

	pthread_mutex_lock(&sim->coders_mutex);
	sim->sim_start = get_time_ms();
	i = -1;
	while (++i < sim->n_coders)
		sim->coders[i].last_compile = sim->sim_start;
	pthread_mutex_unlock(&sim->coders_mutex);
	pthread_mutex_lock(&sim->stop_mutex);
	sim->can_start = 1;
	pthread_mutex_unlock(&sim->stop_mutex);
}

int	main(int ac, char **av)
{
	t_sim	sim;
	int		i;

	if (ac != 9)
	{
		fprintf(stderr,
			"Usage: %s n_coders time_burnout time_compile time_debug "
			"time_refactor n_compiles dongle_cd scheduler\n", av[0]);
		return (ERR_ARGC);
	}
	memset(&sim, 0, sizeof(t_sim));
	if (parsing(av, &sim))
	{
		fprintf(stderr, "Error: invalid arguments\n");
		return (ERR_PARSING);
	}
	i = init_sim(&sim);
	if (i != 0)
		return (i);
	while (i < sim.n_coders)
	{
		pthread_join(sim.coders[i].thread, NULL);
		i++;
	}
	return (free_return(&sim, 3, 0, 0));
}
