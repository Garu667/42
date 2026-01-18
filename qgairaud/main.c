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

static void	choose_algo(t_stack *a, t_stack *b, int flag)
{
	if (flag == FLAG_SIMPLE)
		selection_sort(a, b);
	else if (flag == FLAG_MEDIUM)
		chunk_sort(a, b);
	else if (flag == FLAG_COMPLEXE)
		radix_sort(a, b);
	else if (flag == FLAG_ADAPTIVE)
	{
		if (a->size <= 5)
			tiny_sort(a, b);
		else
			chunk_sort(a, b);
	}
}

static void	push_swap(t_stack *a, int flag)
{
	t_stack	b;

	b.head = NULL;
	b.size = 0;
	stack_to_index(a);
	choose_algo(a, &b, flag);
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
    push_swap(&a, FLAG_ADAPTIVE);
    printf("\nAprès tri :\n\n");
    print_stack(&a);
	free_stack(&a);
	return (0);
}