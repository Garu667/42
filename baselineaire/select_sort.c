/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   select_sort.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 09:29:00 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

void	selection_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	// int	pos;

	// bench->strats |= FLAG_SIMPLE;
	if (!a || is_sorted(a) || !b)
		return ;
	while (a->size)
	{
		bring_min_top(a, b, bench);
		bench->op(a, b, bench, "pb\n");
	}
	while (b->size)
		bench->op(a, b, bench, "pa\n");
}
