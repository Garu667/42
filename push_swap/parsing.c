/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 07:15:59 by ramaroud          #+#    #+#             */
/*   Updated: 2025/12/13 07:16:01 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static bool	is_double(int *tab, int indx, int nbr)
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

static void	realloc_tab(t_stack *stack, int size)
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

static void	parse_one(char *str, t_stack *stack)
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

static void	parse_multiple(char **av, int len, t_stack *stack)
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
