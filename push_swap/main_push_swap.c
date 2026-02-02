/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_push_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:32:47 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:32:47 by ramaroud         ###   ########lyon.fr   */
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

void	choose_algo(t_stack *a, t_stack *b, int flag)
{
	t_bench	bench;

	bench.strats = -1;
	bench.op = do_op_nobench;
	if (flag & FLAG_BENCH)
		setup_benchmark(&bench, a->disorder, flag);
	if (flag & FLAG_SIMPLE)
		selection_sort(a, b, &bench);
	else if (flag & FLAG_MEDIUM)
		chunk_sort(a, b, &bench);
	else if (flag & FLAG_COMPLEX)
		radix_sort(a, b, &bench);
	else if ((flag & FLAG_ADAPTIVE) || !flag || (flag & FLAG_BENCH))
	{
		if (a->disorder < 0.2f)
			selection_sort(a, b, &bench);
		else if (a->disorder >= 0.2f && a->disorder < 0.5f)
			chunk_sort(a, b, &bench);
		else if (a->disorder >= 0.5f)
			radix_sort(a, b, &bench);
	}
	if (flag & FLAG_BENCH)
		print_benchmark(&bench, a);
}

void	push_swap(t_stack *a, int flag)
{
	t_stack	b;

	b.size = 0;
	b.disorder = 0.0f;
	b.head = NULL;
	stack_to_index(a);
	choose_algo(a, &b, flag);
	free_all(&b, NULL, 3);
}

int	main(int ac, char **av)
{
	t_stack	a;
	int		flag;

	a.size = 0;
	a.head = NULL;
	if (ac < 2)
		return (1);
	flag = ft_check_flag(av, ac);
	if (flag == -1)
		exit(write(2, "Error\n", 6));
	if (parsing(&a, ac, av) || !a.head)
		return (write(2, "Error\n", 6));
	a.disorder = ft_compute_disorder(a);
	push_swap(&a, flag);
	free_all(&a, NULL, 3);
	return (0);
}
