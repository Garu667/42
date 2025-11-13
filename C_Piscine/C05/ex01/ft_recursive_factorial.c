int		ft_recursive_factorial_recur(int i, int n)
{
	if (i == 0)
		return (n);
	if (i >= 0)
		return (ft_recursive_factorial_recur(i - 1, n * i));
	return (0);
}

int		ft_recursive_factorial(int nb)
{
	return (ft_recursive_factorial_recur(nb, 1));
}

