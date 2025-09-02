void	*ft_memcpy(void *s, int c, int n)
{
	unsigned char	*ptr;
	int	i;

	i = -1;
	ptr = s;
	while (++i < n)
		ptr[i] = c;
	return (s);
}

