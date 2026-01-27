/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   selection_sort.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/27 14:34:05 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

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
