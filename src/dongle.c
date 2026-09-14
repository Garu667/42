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

static int	free_now(t_dongle *d, long cd)
{
	return (!d->in_use && get_time_ms() - d->released_at >= cd);
}

static int	dongle_ready(t_sim *sim, t_dongle *d, t_waiter *w)
{
	t_waiter	*head;

	if (!free_now(d, sim->dongle_cd))
		return (0);
	head = heap_peek(d);
	if (head == w || head == NULL)
		return (1);
	return (0);
}

int	try_claim(t_coder *c)
{
	int	ok;

	lock_pair(c);
	ok = (dongle_ready(c->sim, c->left, &c->waiter)
			&& dongle_ready(c->sim, c->right, &c->waiter));
	if (ok)
	{
		c->left->in_use = 1;
		c->right->in_use = 1;
		heap_remove(c->left, &c->waiter);
		heap_remove(c->right, &c->waiter);
	}
	unlock_pair(c);
	return (ok);
}

void	release_pair(t_coder *c)
{
	pthread_mutex_lock(&c->sim->table_mutex);
	lock_pair(c);
	c->left->in_use = 0;
	c->left->released_at = get_time_ms();
	c->right->in_use = 0;
	c->right->released_at = get_time_ms();
	unlock_pair(c);
	pthread_cond_broadcast(&c->sim->table_cond);
	pthread_mutex_unlock(&c->sim->table_mutex);
}
