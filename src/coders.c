/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coders.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/27 15:01:49 by ramaroud          #+#    #+#             */
/*   Updated: 2026/07/27 15:01:49 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	log_action(t_sim *sim, int coder_id, char *action)
{
	pthread_mutex_lock(&sim->log_mutex);
	if (!sim_should_stop(sim))
		printf("%ld %d %s\n", get_elapsed_ms(sim), coder_id, action);
	pthread_mutex_unlock(&sim->log_mutex);
}

static void	coder_compile(t_sim *sim, t_coder *coder)
{
	pthread_mutex_lock(&sim->coders_mutex);
	coder->last_compile = get_time_ms();
	pthread_mutex_unlock(&sim->coders_mutex);
	log_action(sim, coder->id, "is compiling");
	ft_msleep(sim->time_compile, sim);
	pthread_mutex_lock(&sim->coders_mutex);
	coder->compile_count++;
	pthread_mutex_unlock(&sim->coders_mutex);
}

static void	coder_life(t_sim *sim, t_coder *coder)
{
	if (coder->left == coder->right)
	{
		log_action(sim, coder->id, "has taken a dongle");
		while (!sim_should_stop(sim))
			usleep(200);
		return ;
	}
	if (sim_should_stop(sim))
		return ;
	if (!request_dongles(coder))
		return ;
	log_action(sim, coder->id, "has taken a dongle");
	log_action(sim, coder->id, "has taken a dongle");
	coder_compile(sim, coder);
	release_dongles(coder);
	if (sim_should_stop(sim))
		return ;
	log_action(sim, coder->id, "is debugging");
	ft_msleep(sim->time_debug, sim);
	if (sim_should_stop(sim))
		return ;
	log_action(sim, coder->id, "is refactoring");
	ft_msleep(sim->time_refactor, sim);
}

void	*coder_routine(void *arg)
{
	t_sim	*sim;
	t_coder	*coder;

	coder = (t_coder *)arg;
	sim = coder->sim;
	if (coder->id % 2 == 0)
		usleep(sim->time_compile * 500);
	while (!sim_should_stop(sim))
	{
		pthread_mutex_lock(&sim->coders_mutex);
		if (coder->compile_count >= sim->n_req_compiles)
		{
			pthread_mutex_unlock(&sim->coders_mutex);
			return (NULL);
		}
		pthread_mutex_unlock(&sim->coders_mutex);
		coder_life(sim, coder);
	}
	return (NULL);
}

long	coder_status(t_sim *sim, int i, int *done)
{
	long	time;

	pthread_mutex_lock(&sim->coders_mutex);
	*done = (sim->coders[i].compile_count >= sim->n_req_compiles);
	time = get_time_ms() - sim->coders[i].last_compile;
	pthread_mutex_unlock(&sim->coders_mutex);
	return (time);
}
