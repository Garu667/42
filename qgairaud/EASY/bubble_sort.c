void	bubble_sort(t_stack *a)
{
	int	turns;
	int	i;

	if (!a || a->size < 2 || is_sorted(a))
		return ;
	turns = a->size - 1;
	while (turns > 0)
	{
		i = 0;
		while (i < turns)
		{
			if (a->head->value > a->head->next->value)
				sa(a, true);
			ra(a, true);
			i++;
		}
		while (i > 0)
		{
			rra(a, true);
			i--;
		}
		turns--;
	}
}
