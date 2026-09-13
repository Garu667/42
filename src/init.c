/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 16:06:15 by ramaroud          #+#    #+#             */
/*   Updated: 2026/07/27 16:06:15 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_dongles(t_dongle *dongles, int n_dongle)
{
	int	i;

	i = 0;
	while (i < n_dongle)
	{
		dongles[i].queue = malloc(n_dongle * sizeof(t_waiter *));
		if (dongles[i].queue == NULL)
		{
			while (--i >= 0)
				free(dongles[i].queue);
			return (-1);
		}
		dongles[i].queue_size = 0;
		dongles[i].queue_cap = n_dongle;
		dongles[i].id = i + 1;
		pthread_mutex_init(&dongles[i].mutex, NULL);
		dongles[i].in_use = 0;
		dongles[i].released_at = 0;
		i++;
	}
	return (0);
}

static void	init_coders(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->n_coders)
	{
		sim->coders[i].id = i + 1;
		sim->coders[i].sim = sim;
		sim->coders[i].left = &sim->dongles[i];
		sim->coders[i].right = &sim->dongles[(i + 1) % sim->n_coders];
		sim->coders[i].last_compile = get_time_ms();
		sim->coders[i].compile_count = 0;
		i++;
	}
}

void	init_unbreakable(t_sim *sim)
{
	init_coders(sim);
	pthread_mutex_init(&sim->table_mutex, NULL);
	pthread_cond_init(&sim->table_cond, NULL);
	pthread_mutex_init(&sim->stop_mutex, NULL);
	pthread_mutex_init(&sim->log_mutex, NULL);
	pthread_mutex_init(&sim->coders_mutex, NULL);
	sim->sim_start = get_time_ms();
}

int	init_sim(t_sim *sim)
{
	int	i;

	i = -1;
	sim->coders = malloc(sim->n_coders * sizeof(t_coder));
	if (!sim->coders)
		return (free_return(sim, 0, ERR_ALLOC_CODERS, 0));
	sim->dongles = malloc(sim->n_coders * sizeof(t_dongle));
	if (!sim->dongles)
		return (free_return(sim, 1, ERR_ALLOC_DONGLES, 0));
	if (init_dongles(sim->dongles, sim->n_coders) != 0)
		return (free_return(sim, 2, ERR_INIT_DONGLES, 0));
	init_unbreakable(sim);
	if (pthread_create(&sim->monitor, NULL, monitor_routine, sim))
		return (free_return(sim, 3, ERR_THREAD_CREATE, 0));
	while (++i < sim->n_coders)
	{
		if (pthread_create(&sim->coders[i].thread, NULL,
				coder_routine, &sim->coders[i]) != 0)
			return (free_return(sim, 4, ERR_THREAD_CREATE, i));
	}
	pthread_join(sim->monitor, NULL);
	return (0);
}
