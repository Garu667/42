int	find_min_position(t_stack *a)
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

void	bring_min_to_top(t_stack *a)
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

void	min_sort(t_stack *a, t_stack *b)
{
	if (!a || is_sorted(a))
		return ;
	while (a->size > 1)
	{
		bring_min_to_top(a);
		pb(b, a, true);
	}
	while (b->size > 0)
		pa(a, b, true);
}
