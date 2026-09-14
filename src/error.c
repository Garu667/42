/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/08 11:14:17 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/08 11:14:17 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	cleanup_sim(t_sim *sim, int i)
{
	int	j;

	j = sim->n_coders;
	if (i != 0)
	{
		j = i;
		i = 0;
	}
	while (i < j)
	{
		free(sim->dongles[i].queue);
		pthread_mutex_destroy(&sim->dongles[i].mutex);
		i++;
	}
	free(sim->dongles);
	free(sim->coders);
	pthread_mutex_destroy(&sim->stop_mutex);
	pthread_mutex_destroy(&sim->log_mutex);
	pthread_mutex_destroy(&sim->coders_mutex);
	pthread_mutex_destroy(&sim->table_mutex);
	pthread_cond_destroy(&sim->table_cond);
}

void	abort_sim(t_sim *sim, int created)
{
	int	i;

	i = -1;
	stop_simulation(sim);
	while (++i < created)
		pthread_join(sim->coders[i].thread, NULL);
	pthread_join(sim->monitor, NULL);
	cleanup_sim(sim, 0);
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
		cleanup_sim(sim, 0);
	if (n_free == 4)
		abort_sim(sim, i);
	return (ret_flag);
}
