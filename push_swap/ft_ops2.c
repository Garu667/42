/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_ops2.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 06:54:08 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/13 06:54:10 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	ra(t_stack *a, bool write_switch)
{
	int	i;
	int	temp;

	if (a->size < 2)
		return (0);
	i = 0;
	temp = a->tab[0];
	while (i < (a->size - 1))
	{
		a->tab[i] = a->tab[i + 1];
		i++;
	}
	a->tab[a->size - 1] = temp;
	if (write_switch)
		ft_safe_write(1, "ra\n", 3);
	return (1);
}

int	rb(t_stack *b, bool write_switch)
{
	int	i;
	int	temp;

	if (b->size < 2)
		return (0);
	i = 0;
	temp = b->tab[0];
	while (i < (b->size - 1))
	{
		b->tab[i] = b->tab[i + 1];
		i++;
	}
	b->tab[b->size - 1] = temp;
	if (write_switch)
		ft_safe_write(1, "rb\n", 3);
	return (1);
}

int	rr(t_stack *a, t_stack *b, bool write_switch)
{
	ra(a, 0);
	rb(b, 0);
	if (write_switch)
		ft_safe_write(1, "rr\n", 3);
	return (1);
}

int	rra(t_stack *a, bool write_switch)
{
	int	i;
	int	temp;

	if (a->size < 2)
		return (0);
	i = a->size - 1;
	temp = a->tab[a->size - 1];
	while (i > 0)
	{
		a->tab[i] = a->tab[i - 1];
		i--;
	}
	a->tab[0] = temp;
	if (write_switch)
		ft_safe_write(1, "rra\n", 4);
	return (1);
}

int	rrb(t_stack *b, bool write_switch)
{
	int	i;
	int	temp;

	if (b->size < 2)
		return (0);
	i = b->size - 1;
	temp = b->tab[b->size - 1];
	while (i > 0)
	{
		b->tab[i] = b->tab[i - 1];
		i--;
	}
	b->tab[0] = temp;
	if (write_switch)
		ft_safe_write(1, "rrb\n", 4);
	return (1);
}
