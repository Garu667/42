#include "header.h"

static int	define_chunks_size(int size)
{
	if (size <= 10)
		return (3);
	return (5);
}

void	chunk_sort(t_stack *a, t_stack *b)
{
	int	chunks_size;
	int	min;
	int	max;

	if (!a || is_sorted(a) || !b)
		return ;
	printf("Chunk sort\n");
	chunks_size = define_chunks_size(a->size);
	min = 0;
	max = chunks_size - 1;
	while (a->size > 0)
	{
		chunk_pb(a, b, min, max);
		min = min + chunks_size;
		max = max + chunks_size;
		if (max >= a->size + b->size)
			max = a->size + b->size - 1;
	}
	while (b->size > 0)
		chunk_pa(a, b);
}
