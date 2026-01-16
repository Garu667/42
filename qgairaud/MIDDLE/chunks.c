static int	define_chunks_size(int size)
{
	if (size <= 100)
		return (30);
	return (50);
}

void	chunk_sort(t_stack *a, t_stack *b)
{
	int	chunks_size;
	int	min;
	int	max;

	if (!a || is_sorted(a) || !b)
		return ;
	chunks_size = define_chunks_size(a->size);
	min = 0;
	max = chunks_size - 1;
	while (a->size > 0)
	{
		push_to_b(a, b, min, max);
		min = min + chunks_size;
		max = max + chunks_size;
		if (max >= a->size + b->size)
			max = a->size + b->size - 1;
	}
	while (b->size > 0)
		push_to_a(a, b);
}
