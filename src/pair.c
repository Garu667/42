/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pair.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/12 10:00:00 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/12 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	lock_pair(t_coder *c)
{
	if (c->left->id < c->right->id)
	{
		pthread_mutex_lock(&c->left->mutex);
		pthread_mutex_lock(&c->right->mutex);
	}
	else
	{
		pthread_mutex_lock(&c->right->mutex);
		pthread_mutex_lock(&c->left->mutex);
	}
}

void	unlock_pair(t_coder *c)
{
	pthread_mutex_unlock(&c->left->mutex);
	pthread_mutex_unlock(&c->right->mutex);
}

void	queue_pair(t_coder *c, int add)
{
	pthread_mutex_lock(&c->left->mutex);
	if (add)
		heap_push(c->left, &c->waiter, c->sim->scheduler);
	else
		heap_remove(c->left, &c->waiter);
	pthread_mutex_unlock(&c->left->mutex);
	pthread_mutex_lock(&c->right->mutex);
	if (add)
		heap_push(c->right, &c->waiter, c->sim->scheduler);
	else
		heap_remove(c->right, &c->waiter);
	pthread_mutex_unlock(&c->right->mutex);
}
