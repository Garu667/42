#include "header.h"

static int	find_min_position(t_stack *a)
{
	t_node	*current;
	int		i;
	int		min_value;
	int		position;

	current = a->head;
	min_value = current->value;
	position = 0;
	i = 0;
	while (current)
	{
		if (current->value < min_value)
		{
			min_value = current->value;
			position = i;
		}
		current = current->next;
		i++;
	}
	return (position);
}

static void	bring_min_top(t_stack *a)
{
	int	position;

	position = find_min_position(a);
	if (position <= a->size / 2)
	{
		while (position > 0)
		{
			ra(a, true);
			position--;
		}
	}
	else
	{
		while (position < a->size)
		{
			rra(a, true);
			position++;
		}
	}
}

void	selection_sort(t_stack *a, t_stack *b)
{
	if (!a || is_sorted(a) || !b)
		return ;
	printf("Selection sort\n");
	while (a->size > 1)
	{
		bring_min_top(a);
		pb(b, a, true);
	}
	while (b->size > 0)
		pa(a, b, true);
}
