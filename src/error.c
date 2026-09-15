/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   error.c                                             :+:      :+:    :+:  */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/08 11:14:17 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	cleanup_sim(t_sim *sim)
{
	int	i;

	i = -1;
	while (++i < sim->n_coders)
	{
		pthread_cond_destroy(&sim->coders[i].cond);
		pthread_mutex_destroy(&sim->dongles[i].mutex);
	}
	free(sim->queue);
	free(sim->dongles);
	free(sim->coders);
	pthread_mutex_destroy(&sim->sched_mutex);
	pthread_cond_destroy(&sim->sched_cond);
	pthread_mutex_destroy(&sim->stop_mutex);
	pthread_mutex_destroy(&sim->log_mutex);
	pthread_mutex_destroy(&sim->coders_mutex);
}

static void	abort_sim(t_sim *sim, int created)
{
	int	i;

	i = -1;
	stop_simulation(sim);
	while (++i < created)
		pthread_join(sim->coders[i].thread, NULL);
	pthread_join(sim->monitor, NULL);
	pthread_join(sim->arbiter, NULL);
	cleanup_sim(sim);
}

static void	abort_arbiter(t_sim *sim)
{
	stop_simulation(sim);
	pthread_join(sim->arbiter, NULL);
	cleanup_sim(sim);
}

int	free_return(t_sim *sim, int n_free, int ret_flag, int i)
{
	if (n_free == 1)
		free(sim->coders);
	if (n_free == 2)
	{
		free(sim->coders);
		free(sim->dongles);
	}
	if (n_free == 3)
		cleanup_sim(sim);
	if (n_free == 4)
		abort_sim(sim, i);
	if (n_free == 5)
		abort_arbiter(sim);
	return (ret_flag);
}
