#include "header.h"

static int	get_position(t_stack *stack, int max)
{
	t_node	*current;
	int		pos;

	current = stack->head;
	pos = 0;
	while (current)
	{
		if (current->index == max)
			return (pos);
		current = current->next;
		pos++;
	}
	return (-1);
}

static int	find_max_one(t_stack *b)
{
	t_node	*current;
	int		max;

	current = b->head;
	max = current->index;
	while (current)
	{
		if (current->index > max)
			max = current->index;
		current = current->next;
	}
	return (max);
}

void	chunk_pa(t_stack *a, t_stack *b)
{
	int	max;
	int	position;

	max = find_max_one(b);
	position = get_position(b, max);
	while (b->head->index != max)
	{
		if (position <= b->size / 2)
			rb(b, true);
		else
			rrb(b, true);
	}
	pa(a, b, true);
}
