/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ramaroud.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 01:53:19 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/13 01:53:21 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

char	*ft_substr(char *s, unsigned int start, size_t len)
{
	size_t	i;
	char	*substr;

	i = 0;
	if (len > ft_strlen(s + start))
		len = ft_strlen(s + start);
	substr = malloc(sizeof(char) * (len + 1));
	if (!substr)
		return (NULL);
	while (i < len)
	{
		substr[i] = s[start + i];
		i++;
	}
	substr[i] = 0;
	return (substr);
}

char	*ft_strchr(char *s, int c)
{
	int	i;

	i = 0;
	while (s[i])
	{
		if (s[i] == (char)c)
			return ((char *)s + i);
		i++;
	}
	if (s[i] == (char)c)
		return ((char *)s + i);
	return (NULL);
}

char	*ft_strtrim(char *s1, char *set)
{
	size_t	j;

	if (!s1 || !set)
		return (0);
	while (*s1 && ft_strchr(set, *s1))
		s1++;
	j = ft_strlen(s1);
	while (j != 0 && ft_strchr(set, s1[j]))
		j--;
	return (ft_substr(s1, 0, j + 1));
}

void	ft_putnbr_fd(int n, int fd)
{
	char	c;

	if (n == -2147483648)
	{
		ft_safe_write(fd, "-2147483648", 11);
		return ;
	}
	if (n < 0)
	{
		ft_safe_write(fd, "-", 1);
		n = -n;
	}
	if (n < 10)
	{
		c = (n + 48);
		ft_safe_write(fd, &c, 1);
	}
	if (n > 9)
	{
		ft_putnbr_fd((n / 10), fd);
		c = ((n % 10) + 48);
		ft_safe_write(fd, &c, 1);
	}
}

void	ft_safe_write(int fd, char *str, int len)
{
	if (write(fd, str, len) == -1)
	{
		write(2, "Error\n", 6);
		exit(EXIT_FAILURE);
	}
}

int	ft_putstr_fd(char *s, int fd)
{
	size_t	i;

	i = -1;
	while (s[++i])
		write(fd, &s[i], 1);
	return (i);
}

float	ft_compute_disorder(t_stack stack)
{
	int	mistake;
	int	pairs;
	int	i;
	int	j;

	i = 0;
	j = 0;
	pairs = 0;
	mistake = 0;
	while (i < (stack.size - 1))
	{
		j = i + 1;
		while (j < stack.size)
		{
			pairs++;
			if (stack.tab[i] > stack.tab[j])
				mistake++;
			j++;
		}
		i++;
	}
	if (pairs == 0)
		return (0);
	return ((float)mistake / (float)pairs);
}

int	ft_strncmp(char *s1, char *s2, size_t n)
{
	size_t	i;

	i = 0;
	while (i < n && (s1[i] || s2[i]))
	{
		if (s1[i] != s2[i])
			return ((unsigned char)s1[i] - (unsigned char)s2[i]);
		i++;
	}
	return (0);
}

int	ft_atoi(const char *str, int *nbr)
{
	int	sign;
	int	i;
	int	j;

	i = 0;
	j = 0;
	sign = 1;
	*nbr = 0;
	while ((str[i] >= 9 && str[i] <= 13) || str[i] == 32)
		i++;
	if (str[i] == '-' || str[i] == '+')
	{
		if (str[i] == '-')
			sign *= -1;
		i += ++j;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		*nbr = *nbr * 10 + (str[i++] - 48);
		j++;
	}
	*nbr *= sign;
	if (j == 0)
		exit(write(2, "Error\n", 6));
	return (j);
}

static void	ft_check2(int *flag, int *count, int flag_bits)
{
	if (flag_bits == FLAG_BENCH)
	{
		(*flag) |= flag_bits;
		(*count)++;
		return ;
	}
	if ((*flag) & (FLAG_SIMPLE | FLAG_MEDIUM | FLAG_COMPLEXE | FLAG_ADAPTIVE))
		exit(write(2, "Error\n", 6));
	(*flag) |= flag_bits;
	(*count)++;
}

static int	ft_check(char *str, int *flag)
{
	int	count;

	count = 0;
	if (ft_strncmp(str, "--bench", 7) == 0)
		ft_check2(flag, &count, FLAG_BENCH);
	else if (ft_strncmp(str, "--simple", 8) == 0)
		ft_check2(flag, &count, FLAG_SIMPLE);
	else if (ft_strncmp(str, "--medium", 8) == 0)
		ft_check2(flag, &count, FLAG_MEDIUM);
	else if (ft_strncmp(str, "--complexe", 10) == 0)
		ft_check2(flag, &count, FLAG_COMPLEXE);
	else if (ft_strncmp(str, "--adaptive", 10) == 0)
		ft_check2(flag, &count, FLAG_ADAPTIVE);
	else
		exit(write(2, "Error\n", 6));
	return (count);
}

int	ft_check_flag(char **av, int *i)
{
	int	flag;
	int	ret;
	int	j;

	if (av[*i][0] != '-' && av[*i][1] != '-')
		return (0);
	flag = 0;
	ret = 0;
	j = 0;
	while (av[*i + j] && j < 2)
	{
		if (av[*i + j][0] == '-' && av[*i + j][1] == '-')
			ret += ft_check(av[(*i) + j], &flag);
		else
			break ;
		j++;
	}
	(*i) += ret;
	return (flag);
}

bool	is_double(int *tab, int indx, int nbr)
{
	int	i;

	i = -1;
	if (indx <= 0 || !tab)
		return (false);
	while (++i < indx)
		if (tab[i] == nbr)
			return (true);
	return (false);
}

void	realloc_tab(t_stack *stack, int size)
{
	int	*new_tab;
	int	i;

	i = 0;
	new_tab = malloc((size + 1) * sizeof(int));
	if (!new_tab)
		exit(write(2, "Error\n", 6));
	while (i < stack->size)
	{
		new_tab[i] = stack->tab[i];
		i++;
	}
	if (stack->tab)
		free(stack->tab);
	stack->tab = new_tab;
	stack->size++;
}

bool	ft_isalnum(int c)
{
	if (c >= 'a' && c <= 'z')
		return (true);
	if (c >= 'A' && c <= 'Z')
		return (true);
	if (c >= '0' && c <= '9')
		return (true);
	return (false);
}

void	parse_one(char *str, t_stack *stack)
{
	int	nbr;
	int	i;
	int	j;

	j = 0;
	i = 0;
	stack->size = 0;
	stack->tab = NULL;
	str = ft_strtrim(str, "\n\t");
	while (str[i] && str[i + 1])
	{
		while (!ft_isalnum(str[i]) && str[i] != '-' && str[i] != '+')
			i++;
		i += ft_atoi((str + i), &nbr);
		if (nbr >= INT_MAX || nbr <= INT_MIN
			|| is_double(stack->tab, j, nbr))
			exit(write(2, "Error\n", 6));
		if (j >= stack->size)
			realloc_tab(stack, (j + 1));
		stack->tab[j] = nbr;
		j++;
	}
}

void	parse_multiple(char **av, int len, t_stack *stack)
{
	int	nbr;
	int	i;

	i = 0;
	stack->size = len;
	stack->tab = malloc(len * sizeof(int));
	while (i < len)
	{
		ft_atoi(av[i], &nbr);
		if (nbr >= INT_MAX || nbr <= INT_MIN
			|| is_double(stack->tab, (i - 1), nbr))
			exit(write(2, "Error\n", 6));
		stack->tab[i] = nbr;
		i++;
	}
}

t_stack	parsing(int *ac, char **av, int i)
{
	t_stack	a;
	int		flag;

	flag = ft_check_flag(av, &i);
	if (flag == -1)
		exit(write(2, "Error\n", 6));
	if ((i + 1) == (*ac))
		parse_one(av[i], &a);
	else
		parse_multiple((av + i), ((*ac) - i), &a);
	(*ac) = flag;
	return (a);
}

int	min_index(t_stack *a)
{
	int	min;
	int	i;
	int	j;

	i = 1;
	j = 0;
	min = a->tab[0];
	while (i < a->size)
	{
		if (a->tab[i] < min)
		{
			min = a->tab[i];
			j = i;
		}
		i++;
	}
	return (j);
}

void	do_op_bench(t_stack *a, t_stack *b, t_bench *bench, char *op)
{
	if (ft_strncmp(op, "sa\n", 3) == 0)
		bench->ops[0] += sa(a, 1);
	else if (ft_strncmp(op, "sb\n", 3) == 0)
		bench->ops[1] += sb(b, 1);
	else if (ft_strncmp(op, "ss\n", 3) == 0)
		bench->ops[2] += ss(a, b, 1);
	else if (ft_strncmp(op, "pa\n", 3) == 0)
		bench->ops[3] += pa(a, b, 1);
	else if (ft_strncmp(op, "pb\n", 3) == 0)
		bench->ops[4] += pb(a, b, 1);
	else if (ft_strncmp(op, "ra\n", 3) == 0)
		bench->ops[5] += ra(a, 1);
	else if (ft_strncmp(op, "rb\n", 3) == 0)
		bench->ops[6] += rb(b, 1);
	else if (ft_strncmp(op, "rr\n", 3) == 0)
		bench->ops[7] += rr(a, b, 1);
	else if (ft_strncmp(op, "rra\n", 4) == 0)
		bench->ops[8] += rra(a, 1);
	else if (ft_strncmp(op, "rrb\n", 4) == 0)
		bench->ops[9] += rrb(b, 1);
	else if (ft_strncmp(op, "rrr\n", 4) == 0)
		bench->ops[10] += rrr(a, b, 1);
}

void	do_op_nobench(t_stack *a, t_stack *b, t_bench *bench, char *op)
{
	(void)bench;
	if (ft_strncmp(op, "sa\n", 3) == 0)
		sa(a, 1);
	else if (ft_strncmp(op, "sb\n", 3) == 0)
		sb(b, 1);
	else if (ft_strncmp(op, "ss\n", 3) == 0)
		ss(a, b, 1);
	else if (ft_strncmp(op, "pa\n", 3) == 0)
		pa(a, b, 1);
	else if (ft_strncmp(op, "pb\n", 3) == 0)
		pb(a, b, 1);
	else if (ft_strncmp(op, "ra\n", 3) == 0)
		ra(a, 1);
	else if (ft_strncmp(op, "rb\n", 3) == 0)
		rb(b, 1);
	else if (ft_strncmp(op, "rr\n", 3) == 0)
		rr(a, b, 1);
	else if (ft_strncmp(op, "rra\n", 4) == 0)
		rra(a, 1);
	else if (ft_strncmp(op, "rrb\n", 4) == 0)
		rrb(b, 1);
	else if (ft_strncmp(op, "rrr\n", 4) == 0)
		rrr(a, b, 1);
}

void	select_sort(t_stack *a, t_stack *b, t_bench *bench)
{
	int	index;

	bench->strats |= FLAG_SIMPLE;
	while (a->size)
	{
		index = min_index(a);
		if (index <= (a->size / 2))
		{
			while (index-- > 0)
				bench->op(a, b, bench, "ra\n");
		}
		else
		{
			index = a->size - index;
			while (index-- > 0)
				bench->op(a, b, bench, "rra\n");
		}
		bench->op(a, b, bench, "pb\n");
	}
	while (b->size)
		bench->op(a, b, bench, "pa\n");
}

void	print_disorder(t_bench *bench)
{
	int	before;
	int	after;

	bench->disorder *= 100;
	before = (int)bench->disorder;
	after = (int)((bench->disorder - before) * 100);
	ft_safe_write(2, "[bench] disorder: ", 19);
	ft_putnbr_fd(before, 2);
	ft_safe_write(2, ".", 1);
	if (after < 10)
		ft_safe_write(2, "0", 1);
	ft_putnbr_fd(after, 2);
	ft_safe_write(2, "%\n", 2);
}

void	print_ops(t_bench *bench)
{
	ft_safe_write(2, "[bench] sa: ", 12);
	ft_putnbr_fd(bench->ops[0], 2);
	ft_safe_write(2, " sb: ", 5);
	ft_putnbr_fd(bench->ops[1], 2);
	ft_safe_write(2, " ss: ", 5);
	ft_putnbr_fd(bench->ops[2], 2);
	ft_safe_write(2, " pa: ", 5);
	ft_putnbr_fd(bench->ops[3], 2);
	ft_safe_write(2, " pb: ", 5);
	ft_putnbr_fd(bench->ops[4], 2);
	ft_safe_write(2, "\n[bench] ra: ", 13);
	ft_putnbr_fd(bench->ops[5], 2);
	ft_safe_write(2, " rb: ", 5);
	ft_putnbr_fd(bench->ops[6], 2);
	ft_safe_write(2, " rr: ", 5);
	ft_putnbr_fd(bench->ops[7], 2);
	ft_safe_write(2, " rra: ", 6);
	ft_putnbr_fd(bench->ops[8], 2);
	ft_safe_write(2, " rrb: ", 6);
	ft_putnbr_fd(bench->ops[9], 2);
	ft_safe_write(2, " rrr: ", 6);
	ft_putnbr_fd(bench->ops[10], 2);
	ft_safe_write(2, "\n", 1);
}

void	print_benchmark(t_bench *bench)
{
	int	total_ops;

	print_disorder(bench);
	ft_safe_write(2, "[bench] strategy: ", 19);
	if (bench->strats & FLAG_SIMPLE)
		ft_safe_write(1, "Simple / O(n²)\n", 16);
	else if (bench->strats & FLAG_MEDIUM)
		ft_safe_write(1, "Medium / O(n√n)\n", 16);
	else if (bench->strats & FLAG_COMPLEXE)
		ft_safe_write(1, "Complexe / O(n log n)\n", 22);
	else if (bench->strats & FLAG_ADAPTIVE)
		ft_safe_write(1, "Adaptive / O(n log n)\n", 22);
	total_ops = bench->ops[0] + bench->ops[1] + bench->ops[2] + bench->ops[3]
		+ bench->ops[4] + bench->ops[5] + bench->ops[6] + bench->ops[7]
		+ bench->ops[8] + bench->ops[9] + bench->ops[10];
	ft_safe_write(2, "[bench] total_ops: ", 20);
	ft_putnbr_fd(total_ops, 2);
	ft_safe_write(2, "\n", 1);
	print_ops(bench);
}

t_bench	setup_benchmark(float disorder, int flag)
{
	t_bench	bench;
	int		i;

	i = -1;
	if (flag & FLAG_SIMPLE)
		bench.strats |= FLAG_SIMPLE;
	else if (flag & FLAG_MEDIUM)
		bench.strats |= FLAG_MEDIUM;
	else if (flag & FLAG_COMPLEXE)
		bench.strats |= FLAG_COMPLEXE;
	else if (flag & FLAG_ADAPTIVE)
		bench.strats |= FLAG_ADAPTIVE;
	bench.disorder = disorder;
	bench.op = do_op_bench;
	while (++i < 11)
		bench.ops[i] = 0;
	return (bench);
}

void	choose_algo(t_stack *a, t_stack *b, int flag, float disorder)
{
	t_bench	bench;

	bench.strats = -1;
	bench.op = do_op_nobench;
	if (flag & FLAG_BENCH)
		bench = setup_benchmark(disorder, flag);
	if (flag & FLAG_SIMPLE)
		select_sort(a, b, &bench);
	else if (flag & FLAG_MEDIUM)
		select_sort(a, b, &bench);
	else if (flag & FLAG_COMPLEXE)
		select_sort(a, b, &bench);
	else if (flag & FLAG_ADAPTIVE)
		select_sort(a, b, &bench);
	else if (disorder < 0.2f)
		select_sort(a, b, &bench);
	else if (disorder >= 0.2f && disorder < 0.5f)
		select_sort(a, b, &bench);
	else if (disorder >= 0.5f)
		select_sort(a, b, &bench);
	select_sort(a, b, &bench);
	if (flag & FLAG_BENCH)
		print_benchmark(&bench);
}

void	push_swap(t_stack *a, int flag, float disorder)
{
	t_stack	b;

	b.size = 0;
	b.tab = malloc(a->size * sizeof(int));
	if (!b.tab)
		exit(write(2, "Error\n", 6));
	choose_algo(a, &b, flag, disorder);
	free(b.tab);
}
