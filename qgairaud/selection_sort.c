/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   selection_sort.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 14:16:41 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	selection_sort(t_stack *a, t_stack *b)
{
	if (!a || is_sorted(a) || !b)
		return ;
	printf("\n\t-> Selection sort <- \n");
	while (a->size > 1)
	{
		bring_min_top(a);
		pb(b, a, true);
	}
	while (b->size > 0)
		pa(a, b, true);
}
