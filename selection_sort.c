/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   selection_sort.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:33:21 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:33:21 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	selection_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	if (!a || is_sorted(a) || !b)
		return ;
	if (a->size <= 5)
	{
		tiny_sort(a, b, bench);
		return ;
	}
	while (a->size)
	{
		bring_min_top(a, b, bench);
		bench->op(a, b, bench, "pb\n");
	}
	while (b->size)
		bench->op(a, b, bench, "pa\n");
}
