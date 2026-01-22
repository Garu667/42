/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tiny_sort.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 18:59:46 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static void	sort_two(t_stack *a, t_stack *b, t_bench *bench)
{
	if (a->head->index > a->head->next->index)
		bench->op(a, b, bench, "sa\n");
}

static void	sort_three(t_stack *a, t_stack *b, t_bench *bench)
{
	int	first;
	int	second;
	int	third;

	first = a->head->index;
	second = a->head->next->index;
	third = a->head->next->next->index;
	if (first > second && second < third && first < third)
		bench->op(a, b, bench, "sa\n");
	else if (first > second && second > third)
	{
		bench->op(a, b, bench, "sa\n");
		bench->op(a, b, bench, "rra\n");
	}
	else if (first > second && second < third && first > third)
		bench->op(a, b, bench, "ra\n");
	else if (first < second && second > third && first > third)
		bench->op(a, b, bench, "rra\n");
	else if (first < second && second > third && first < third)
	{
		bench->op(a, b, bench, "sa\n");
		bench->op(a, b, bench, "ra\n");
	}
}

static void	sort_four(t_stack *a, t_stack *b, t_bench *bench)
{
	bring_min_top(a, b, bench);
	bench->op(a, b, bench, "pb\n");
	sort_three(a, b, bench);
	bench->op(a, b, bench, "pa\n");
}

static void	sort_five(t_stack *a, t_stack *b, t_bench *bench)
{
	bring_min_top(a, b, bench);
	bench->op(a, b, bench, "pb\n");
	bring_min_top(a, b, bench);
	bench->op(a, b, bench, "pb\n");
	sort_three(a, b, bench);
	bench->op(a, b, bench, "pa\n");
	bench->op(a, b, bench, "pa\n");
}

void	tiny_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	bench->strats |= FLAG_SIMPLE;
	if (!a || is_sorted(a) || !b)
		return ;
	if (a->size == 2)
		sort_two(a, b, bench);
	else if (a->size == 3)
		sort_three(a, b, bench);
	else if (a->size == 4)
		sort_four(a, b, bench);
	else if (a->size == 5)
		sort_five(a, b, bench);
}
