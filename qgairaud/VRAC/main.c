/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 14:14:48 by qgairaud          #+#    #+#             */
/*   Updated: 2026/01/20 14:40:28 by qgairaud         ###   ########.fr       */
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
	// t_bench	bench;

    disorder = 0.0f;
	// bench.strats = -1;
	// bench.op = do_op_nobench;
	// setup_benchmark(&bench, disorder, flag);
	if (flag == FLAG_SIMPLE)
		selection_sort(a, b);
	else if (flag == FLAG_MEDIUM)
		chunk_sort(a, b);
	else if (flag == FLAG_COMPLEXE)
		radix_sort(a, b);
	else if (flag == FLAG_ADAPTIVE)
		tiny_sort(a, b);
	// print_benchmark(&bench);

}

static void	push_swap(t_stack *a, int flag)
{
	t_stack	b;
	float	disorder;

	b.head = NULL;
	b.size = 0;
	// disorder = ft_compute_disorder(*a);
	disorder = 0.0f;
	stack_to_index(a);
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
    printf("\nAvant tri :\n\n");
    print_stack(&a);
    // push_swap(&a, FLAG_ADAPTIVE);
    push_swap(&a, FLAG_SIMPLE);
    // push_swap(&a, FLAG_MEDIUM);
    // push_swap(&a, FLAG_COMPLEXE);
    printf("\nAprès tri :\n\n");
    print_stack(&a);
	free_stack(&a);
	return (0);
}