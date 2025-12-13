/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_ops.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: bcondemi <bcondemi@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/11 14:29:37 by bcondemi          #+#    #+#             */
/*   Updated: 2025/12/12 19:42:27 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	pa(t_stack *a, t_stack *b, bool write_switch)
{
	int	i;

	if (b->size == 0)
		return (0);
	i = a->size;
	while (i > 0)
	{
		a->tab[i] = a->tab[i - 1];
		i--;
	}
	a->tab[0] = b->tab[0];
	a->size++;
	b->size--;
	i = 0;
	while (i < b->size)
	{
		b->tab[i] = b->tab[i + 1];
		i++;
	}
	if (write_switch)
		ft_safe_write(1, "pa\n", 3);
	return (1);
}

int	pb(t_stack *a, t_stack *b, bool write_switch)
{
	int	i;

	if (a->size == 0)
		return (0);
	i = b->size;
	while (i > 0)
	{
		b->tab[i] = b->tab[i - 1];
		i--;
	}
	b->tab[0] = a->tab[0];
	b->size++;
	a->size--;
	i = 0;
	while (i < a->size)
	{
		a->tab[i] = a->tab[i + 1];
		i++;
	}
	if (write_switch)
		ft_safe_write(1, "pb\n", 3);
	return (1);
}

int	sa(t_stack *a, bool write_switch)
{
	int	tmp;

	if (a->size < 2)
		return (0);
	tmp = a->tab[0];
	a->tab[0] = a->tab[1];
	a->tab[1] = tmp;
	if (write_switch)
		ft_safe_write(1, "sa\n", 3);
	return (1);
}

int	sb(t_stack *b, bool write_switch)
{
	int	tmp;

	if (b->size < 2)
		return (0);
	tmp = b->tab[0];
	b->tab[0] = b->tab[1];
	b->tab[1] = tmp;
	if (write_switch)
		ft_safe_write(1, "sb\n", 3);
	return (1);
}

int	ss(t_stack *a, t_stack *b, bool write_switch)
{
	sa(a, 0);
	sb(b, 0);
	if (write_switch)
		ft_safe_write(1, "ss\n", 3);
	return (1);
}

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

int	rrr(t_stack *a, t_stack *b, bool write_switch)
{
	rra(a, 0);
	rrb(b, 0);
	if (write_switch)
		ft_safe_write(1, "rrr\n", 4);
	return (1);
}
