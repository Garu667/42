/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tiny_sort.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:33:36 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:33:36 by ramaroud         ###   ########lyon.fr   */
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
	third = a->head->prev->index;
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
	int	first;
	int	second;
	int	third;
	int	fourth;

	first = a->head->index;
	second = a->head->next->index;
	third = a->head->next->next->index;
	fourth = a->head->prev->index;
	while (!(is_sorted(a) && b->size == 0))
	{
		if (first > second && first < third && third < fourth)
		{
			bench->op(a, b, bench, "sa\n");
			return ;
		}
		bring_min_top(a, b, bench);
		bench->op(a, b, bench, "pb\n");
		sort_three(a, b, bench);
		bench->op(a, b, bench, "pa\n");
	}
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
	if (!a || !b || is_sorted(a))
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
