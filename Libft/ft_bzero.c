void	ft_bzero(void *s, int n)
{
	int	i;
	char	*str;

	i = -1;
	str = (char *)s;
	while (++i < n)
		str[i] = 0;
}
