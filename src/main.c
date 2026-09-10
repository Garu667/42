/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 14:18:32 by ramaroud          #+#    #+#             */
/*   Updated: 2026/06/11 14:18:32 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*stop_simulation(t_sim *sim)
{
	pthread_mutex_lock(&sim->stop_mutex);
	sim->stop = 1;
	pthread_mutex_unlock(&sim->stop_mutex);
	return (NULL);
}

void	*monitor_routine(void *arg)
{
	t_sim	*sim;
	long	time;
	int		done;
	int		i;

	sim = (t_sim *)arg;
	while (!sim_should_stop(sim))
	{
		i = -1;
		usleep(100);
		while (++i < sim->n_coders)
		{
			time = coder_status(sim, i, &done);
			if (!done && time > sim->time_burnout)
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
		return (2);
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
