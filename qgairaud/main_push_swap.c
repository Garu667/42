/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_push_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:39 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/19 22:23:57 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	choose_algo(t_stack *a, t_stack *b, int flag, float disorder)
{
	t_bench	bench;

	bench.strats = -1;
	bench.op = do_op_nobench;
	if (flag & FLAG_BENCH)
		setup_benchmark(&bench, disorder, flag);
	if (flag & FLAG_SIMPLE)
		selection_sort(a, b);
	else if (flag & FLAG_MEDIUM)
		chunk_sort(a, b);
	else if (flag & FLAG_COMPLEXE)
		radix_sort(a, b);
	else if (flag & FLAG_ADAPTIVE)
	{
		if (disorder < 0.2f)
			selection_sort(a, b);
		else if (disorder >= 0.2f && disorder < 0.5f)
			chunk_sort(a, b);
		else if (disorder >= 0.5f)
			radix_sort(a, b);
	}
	if (flag & FLAG_BENCH)
		print_benchmark(&bench);
}

void	push_swap(t_stack *a, int flag, float disorder)
{
	t_stack	b;

	b.head = NULL;
	b.size = 0;
	choose_algo(a, &b, flag, disorder);
	free_stack(&b);
}

int	main(int ac, char **av)
{
	t_stack	a;

	if (ac < 2)
		return (write(2, "Error\n", 6));
	a = parsing(&ac, av);
	if (!a.head)
		return (write(2, "Error\n", 6));
	push_swap(&a, ac, ft_compute_disorder(a));
	free_stack(&a);
	return (0);
}
