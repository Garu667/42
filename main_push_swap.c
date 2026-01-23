/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_push_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:39 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/23 16:14:46 by qgairaud         ###   ########.fr       */
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
		selection_sort(a, b, &bench);
	else if (flag & FLAG_MEDIUM)
		chunk_sort(a, b, &bench);
	else if (flag & FLAG_COMPLEX)
		radix_sort(a, b, &bench);
	else if ((flag & FLAG_ADAPTIVE) || !flag || (flag & FLAG_BENCH))
	{
		if (disorder < 0.2 && a->size <= 5)
			tiny_sort(a, b, &bench);
		else if (disorder < 0.2f && a->size > 5)
			selection_sort(a, b, &bench);
		else if (disorder >= 0.2f && disorder < 0.5f)
			chunk_sort(a, b, &bench);
		else if (disorder >= 0.5f)
			radix_sort(a, b, &bench);
	}
	if (flag & FLAG_BENCH)
		print_benchmark(&bench);
}

void	push_swap(t_stack *a, int flag, float disorder)
{
	t_stack	b;

	b.size = 0;
	b.head = NULL;
	stack_to_index(a);
	choose_algo(a, &b, flag, disorder);
	free_stack(&b);
}

int	main(int ac, char **av)
{
	t_stack	a;
	float	disorder;
	int		flag;
	int		i;

	i = 1;
	a.size = 0;
	a.head = NULL;
	if (ac < 2)
		return (write(2, "Error\n", 6));
	flag = ft_check_flag(av, &i);
	if (flag == -1)
		exit(write(2, "Error\n", 6));
	parsing(&a, &ac, av, i);
	if (!a.head)
		return (write(2, "Error\n", 6));
	disorder = ft_compute_disorder(a);
	push_swap(&a, flag, disorder);
	free_stack(&a);
	return (0);
}
