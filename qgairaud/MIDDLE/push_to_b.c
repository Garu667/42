static int	is_in_chunk(int index, int min, int max)
{
	if (index >= min && index <= max)
		return (1);
	return (0);
}

void	push_to_b(t_stack *a, t_stack *b, int min, int max)
{
	int	to_push;
	int	pushed;

	to_push = max - min;
	pushed = 0;
	while (pushed <= to_push)
	{
		if (is_in_chunk(a->head->index, min, max))
		{
			pb(b, a, true);
			pushed++;
		}
		else
			ra(a, true);
	}
}
