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

static void	parse_multiple(char **split, t_stack *a)
{
	int	value;
	int	i;

	a->size = 0;
	while (split[a->size])
		a->size++;
	if (a->size == 0)
	{
		a->tab = NULL;
		return ;
	}
	a->tab = malloc(sizeof(int) * a->size);
	if (!a->tab)
		return ;
	i = 0;
	while (i < a->size)
	{
		if (!ft_atoi(split[i], &value) || is_double(a->tab, i, value)
			|| !(value <= INT_MAX && value >= INT_MIN))
			exit(write(2, "Error\n", 6));
		if (is_double(a->tab, i, value))
			exit(write(2, "Error\n", 6));
		a->tab[i] = value;
		i++;
	}
}

static void	parse_one(char *str, t_stack *a)
{
	char	**split;

	split = ft_split(str, ' ');
	if (!split)
	{
		a->tab = NULL;
		return ;
	}
	parse_multiple(split, a);
	free_split(split, a->size, 2);
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
		parse_multiple((av + i), &a);
	(*ac) = flag;
	return (a);
}
