/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_push_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 19:42:14 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/12 19:42:17 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	choose_algo(t_stack *a, t_stack *b, int flag, float disorder)
{
	t_bench	bench;

	bench.strats = -1;
	bench.op = do_op_nobench;
	if (flag & FLAG_BENCH)
		bench = setup_benchmark(disorder, flag);
	if (flag & FLAG_SIMPLE)
		select_sort(a, b, &bench);
	else if (flag & FLAG_MEDIUM)
		select_sort(a, b, &bench);
	else if (flag & FLAG_COMPLEXE)
		select_sort(a, b, &bench);
	else if (flag & FLAG_ADAPTIVE)
		select_sort(a, b, &bench);
	else if (disorder < 0.2f)
		select_sort(a, b, &bench);
	else if (disorder >= 0.2f && disorder < 0.5f)
		select_sort(a, b, &bench);
	else if (disorder >= 0.5f)
		select_sort(a, b, &bench);
	select_sort(a, b, &bench);
	if (flag & FLAG_BENCH)
		print_benchmark(&bench);
}

void	push_swap(t_stack *a, int flag, float disorder)
{
	t_stack	b;

	b.size = 0;
	b.tab = malloc(a->size * sizeof(int));
	if (!b.tab)
		exit(write(2, "Error\n", 6));
	choose_algo(a, &b, flag, disorder);
	free(b.tab);
}

int	main(int ac, char **av)
{
	t_stack	a;
	int		i;

	i = 1;
	if (ac < 1)
		return (write(2, "Error\n", 6));
	a = parsing(&ac, av, i);
	push_swap(&a, ac, ft_compute_disorder(a));
	free(a.tab);
}
