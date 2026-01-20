/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_push_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 14:16:15 by qgairaud          #+#    #+#             */
/*   Updated: 2026/01/20 14:16:16 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	print_stack(t_stack *a)
{
	t_node	*current;

	if (!a || !a->head)
		return;
	current = a->head;
	while (current)
	{
		printf("%d ", current->value);
		current = current->next;
	}
	printf("\n");
}

static void	choose_algo(t_stack *a, t_stack *b, int flag, float disorder)
{
	t_bench	bench;

	// bench.strats = -1;
	// bench.op = do_op_nobench;
	if (flag & FLAG_BENCH)
		setup_benchmark(&bench, disorder, flag);
	// if (flag & FLAG_SIMPLE)
	if (flag == FLAG_SIMPLE)
		selection_sort(a, b);
	// else if (flag & FLAG_MEDIUM)
	else if (flag == FLAG_MEDIUM)
		chunk_sort(a, b);
	// else if (flag & FLAG_COMPLEXE)
	else if (flag == FLAG_COMPLEXE)
		radix_sort(a, b);
	// else if (flag & FLAG_ADAPTIVE || !flag)
	// else if (flag == FLAG_ADAPTIVE)
	// {
	// 	if (disorder < 0.2)
	// 		selection_sort(a, b);
	// 	else if (disorder >= 0.2 && disorder < 0.5)
	// 		chunk_sort(a, b);
	// 	else if (disorder >= 0.5)
	// 		radix_sort(a, b);
	// }
	// print_benchmark(&bench);
}

static void	push_swap(t_stack *a, int flag, float disorder)
{
	t_stack	b;

	b.head = NULL;
	b.size = 0;
	stack_to_index(a);
	choose_algo(a, &b, flag, disorder);
	free_stack(&b);
}

int	main(int ac, char **av)
{
	t_stack	a;
	float	disorder;

	if (ac < 2)
		return (write(2, "Error\n", 6));
	a = parsing(&ac, av);
	if (!a.head)
		return (write(2, "Error\n", 6));
	// disorder = ft_compute_disorder(a);
	disorder = 0.0;
    // printf("\nAvant tri :\n\n");
    // print_stack(&a);
    // push_swap(&a, FLAG_ADAPTIVE);
    // push_swap(&a, FLAG_SIMPLE);
    push_swap(&a, FLAG_MEDIUM, disorder);
    // push_swap(&a, FLAG_COMPLEXE);
    // printf("\nAprès tri :\n\n");
    // print_stack(&a);
	free_stack(&a);
	return (0);
}
