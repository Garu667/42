/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tiny_sort.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 14:16:47 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static void	sort_two(t_stack *a)
{
	if (a->head->index > a->head->next->index)
		sa(a, true);
}

static void	sort_three(t_stack *a)
{
	int	first;
	int	second;
	int	third;

	first = a->head->index;
	second = a->head->next->index;
	third = a->head->next->next->index;
	if (first > second && second < third && first < third)
		sa(a, true);
	else if (first > second && second > third)
	{
		sa(a, true);
		rra(a, true);
	}
	else if (first > second && second < third && first > third)
		ra(a, true);
	else if (first < second && second > third && first > third)
		rra(a, true);
	else if (first < second && second > third && first < third)
	{
		sa(a, true);
		ra(a, true);
	}
}

static void	sort_four(t_stack *a, t_stack *b)
{
	bring_min_top(a);
	pb(b, a, true);
	sort_three(a);
	pa(a, b, true);
}

static void	sort_five(t_stack *a, t_stack *b)
{
	int		position;
	t_node	*current;

	bring_min_top(a);
	pb(b, a, true);
	current = a->head;
	position = 0;
	while (current && current->index != a->size)
	{
		current = current->next;
		position++;
	}
	while (position--)
		ra(a, true);
	pb(b, a, true);
	sort_three(a);
	pa(a, b, true);
	ra(a, true);
	pa(a, b, true);
}

void	tiny_sort(t_stack *a, t_stack *b)
{
	if (!a || is_sorted(a) || !b)
		return ;
	printf("\n\t -> Tiny sort <- \n");
	if (a->size == 2)
		sort_two(a);
	else if (a->size == 3)
		sort_three(a);
	else if (a->size == 4)
		sort_four(a, b);
	else if (a->size == 5)
		sort_five(a, b);
}
