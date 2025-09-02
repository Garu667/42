#include <stdlib.h>

void	*ft_calloc(size_t count, size_t size)
{
	unsigned char	*tmp;
	int	i;

	i = -1;
	tmp = malloc(count * size);
	if (!tmp)
		return (NULL);
	while (++i < (count * size))
		tmp[i] = 0;
	return (tmp);
}
