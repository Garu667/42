/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main_push_swap.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: quentin <quentin@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:39 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/21 13:00:31 by quentin          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../header.h"

void	print_stack(t_stack *stack, char name)
{
	t_node	*current;
	int		i;

	printf("Stack %c (size = %d): ", name, stack->size);
	if (!stack || !stack->head)
	{
		printf("empty\n");
		return ;
	}
	current = stack->head;
	i = 0;
	while (i < stack->size)
	{
		printf("%d", current->value);
		if (i < stack->size - 1)
			printf(" -> ");
		current = current->next;
		i++;
	}
	printf("\n");
}
void	print_stacks(t_stack *a, t_stack *b, char *msg)
{
	printf("\n --> %s <--\n\n", msg);
	print_stack(a, 'A');
	print_stack(b, 'B');
}

void	choose_algo(t_stack *a, t_stack *b, int flag, float disorder)
{
	t_bench	bench;

	bench.strats = -1;
	bench.op = do_op_nobench;
	print_stacks(a, b, "AVANT");
	if (flag & FLAG_BENCH)
		setup_benchmark(&bench, disorder, flag);
	if (flag & FLAG_SIMPLE)
		selection_sort(a, b, &bench);
	else if (flag & FLAG_MEDIUM)
		chunk_sort(a, b, &bench);
	else if (flag & FLAG_COMPLEXE)
		radix_sort(a, b, &bench);
	else if (flag & FLAG_ADAPTIVE || !flag)
	{
		if (disorder < 0.2 && a->size <= 3)
			tiny_sort(a, b, &bench);
		else if (disorder < 0.2f && a->size > 3)
			selection_sort(a, b, &bench);
		else if (disorder >= 0.2f && disorder < 0.5f)
			chunk_sort(a, b, &bench);
		else if (disorder >= 0.5f)
			radix_sort(a, b, &bench);
	}
	if (flag & FLAG_BENCH)
		print_benchmark(&bench);
	print_stacks(a, b, "APRES");
}

void	push_swap(t_stack *a, int flag, float disorder)
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
	disorder = ft_compute_disorder(a);
	if (disorder != 0.0f)
	{
		push_swap(&a, ac, disorder);
	}
	free_stack(&a);
	return (0);
}
