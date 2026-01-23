/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   benchmark.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:06 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 19:27:18 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

float	ft_compute_disorder(t_stack stack)
{
	int		mistake;
	int		pairs;
	t_node	*i;
	t_node	*j;

	if (!stack.head || stack.size <= 1)
		return (0);
	pairs = 0;
	mistake = 0;
	i = stack.head;
	while (i->next != stack.head)
	{
		j = i->next;
		while (j != stack.head)
		{
			pairs++;
			if (i->value > j->value)
				mistake++;
			j = j->next;
		}
		i = i->next;
	}
	if (pairs == 0)
		return (0);
	return ((float)mistake / (float)pairs);
}

static void	print_disorder(t_bench *bench)
{
	int	before;
	int	after;

	bench->disorder *= 100;
	before = (int)bench->disorder;
	after = (int)((bench->disorder - before) * 100);
	ft_safe_write(2, "[bench] disorder: ", 19);
	ft_putnbr_fd(before, 2);
	ft_safe_write(2, ".", 1);
	if (after < 10)
		ft_safe_write(2, "0", 1);
	ft_putnbr_fd(after, 2);
	ft_safe_write(2, "%\n", 2);
}

static void	print_ops(t_bench *bench)
{
	ft_safe_write(2, "[bench] sa: ", 12);
	ft_putnbr_fd(bench->ops[0], 2);
	ft_safe_write(2, " sb: ", 5);
	ft_putnbr_fd(bench->ops[1], 2);
	ft_safe_write(2, " ss: ", 5);
	ft_putnbr_fd(bench->ops[2], 2);
	ft_safe_write(2, " pa: ", 5);
	ft_putnbr_fd(bench->ops[3], 2);
	ft_safe_write(2, " pb: ", 5);
	ft_putnbr_fd(bench->ops[4], 2);
	ft_safe_write(2, "\n[bench] ra: ", 13);
	ft_putnbr_fd(bench->ops[5], 2);
	ft_safe_write(2, " rb: ", 5);
	ft_putnbr_fd(bench->ops[6], 2);
	ft_safe_write(2, " rr: ", 5);
	ft_putnbr_fd(bench->ops[7], 2);
	ft_safe_write(2, " rra: ", 6);
	ft_putnbr_fd(bench->ops[8], 2);
	ft_safe_write(2, " rrb: ", 6);
	ft_putnbr_fd(bench->ops[9], 2);
	ft_safe_write(2, " rrr: ", 6);
	ft_putnbr_fd(bench->ops[10], 2);
	ft_safe_write(2, "\n", 1);
}

void	print_benchmark(t_bench *bench)
{
	int	total_ops;

	print_disorder(bench);
	ft_safe_write(2, "[bench] strategy: ", 19);
	if (bench->strats & FLAG_SIMPLE)
		ft_safe_write(2, "Simple / O(n²)\n", 16);
	else if (bench->strats & FLAG_MEDIUM)
		ft_safe_write(2, "Medium / O(n√n)\n", 16);
	else if (bench->strats & FLAG_COMPLEX)
		ft_safe_write(2, "Complex / O(n log n)\n", 22);
	else if (bench->strats & FLAG_ADAPTIVE)
		ft_safe_write(2, "Adaptive / O(n log n)\n", 22);
	total_ops = bench->ops[0] + bench->ops[1] + bench->ops[2] + bench->ops[3]
		+ bench->ops[4] + bench->ops[5] + bench->ops[6] + bench->ops[7]
		+ bench->ops[8] + bench->ops[9] + bench->ops[10];
	ft_safe_write(2, "[bench] total_ops: ", 20);
	ft_putnbr_fd(total_ops, 2);
	ft_safe_write(2, "\n", 1);
	print_ops(bench);
}

void	setup_benchmark(t_bench *bench, float disorder, int flag)
{
	int		i;

	i = -1;
	bench->strats = flag & ~FLAG_BENCH;
	bench->disorder = disorder;
	bench->op = do_op_bench;
	while (++i < 11)
		bench->ops[i] = 0;
}
