/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_push_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:39 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/15 16:02:39 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

void	choose_algo(t_stack *a, t_stack *b, int flag, float disorder)
{
	t_bench	bench;

	(void)a;
	(void)b;
	bench.strats = -1;
	bench.op = do_op_nobench;
	if (flag & FLAG_BENCH)
		setup_benchmark(&bench, disorder, flag);
	if (flag & FLAG_SIMPLE)
		ft_putstr_fd("Bubble Sort a faire\n", 1);
	else if (flag & FLAG_MEDIUM)
		ft_putstr_fd("Bucket Sort a faire\n", 1);
	else if (flag & FLAG_COMPLEXE)
		ft_putstr_fd("Radix Sort a faire\n", 1);
	else if (flag & FLAG_ADAPTIVE)
		write(1, "Adaptive a faire\n", 17);
	else if (disorder < 0.2f)
		ft_putstr_fd("Bubble Sort a faire\n", 1);
	else if (disorder >= 0.2f && disorder < 0.5f)
		ft_putstr_fd("Bucket Sort a faire\n", 1);
	else if (disorder >= 0.5f)
		ft_putstr_fd("Radix Sort a faire\n", 1);
	else
		write(1, "Adaptive a faire\n", 17);
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
