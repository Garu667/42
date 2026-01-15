/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ramaroud.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 15:43:15 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/13 15:43:15 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include <stdio.h>

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

static bool	is_double(t_stack *stack, int nbr)
{
	t_node	*current;

	if (!stack || !stack->head)
		return (false);
	current = stack->head;
	while (current)
	{
		if (current->value == nbr)
			return (true);
		current = current->next;
		if (current == stack->head)
			break ;
	}
	return (false);
}

static t_node	*create_node(int value)
{
	t_node	*new_node;

	new_node = malloc(sizeof(t_node));
	if (!new_node)
		return (NULL);
	new_node->value = value;
	new_node->index = 0;
	new_node->next = NULL;
	new_node->previous = NULL;
	return (new_node);
}

static void	add_node_back(t_stack *stack, t_node *new_node)
{
	t_node	*current;

	if (!stack->head)
	{
		stack->head = new_node;
		new_node->next = new_node;
		new_node->previous = new_node;
	}
	else
	{
		current = stack->head->previous;
		current->next = new_node;
		new_node->previous = current;
		new_node->next = stack->head;
		stack->head->previous = new_node;
	}
	stack->size++;
}

static void	parse_multiple(char **split, t_stack *a)
{
	int		value;
	int		count;
	int		i;
	t_node	*new_node;

	count = 0;
	while (split[count])
		count++;
	if (count == 0)
		return ;
	i = 0;
	while (i < count)
	{
		if (!ft_atoi(split[i], &value) || !(value <= INT_MAX && value >= INT_MIN) || is_double(a, value))
			exit(write(2, "Error\n", 6));
		new_node = create_node(value);
		if (!new_node)
			exit(write(2, "Error\n", 6));
		add_node_back(a, new_node);
		i++;
	}
}

static void	parse_one(char *str, t_stack *a)
{
	char	**split;
	int		count;

	split = ft_split(str, ' ');
	if (!split)
		return ;
	count = 0;
	while (split[count])
		count++;
	parse_multiple(split, a);
	free_split(split, count, 2);
}

t_stack	parsing(int *ac, char **av, int i)
{
	t_stack	a;
	int		flag;

	a.size = 0;
	a.head = NULL;
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

int	main(int ac, char **av)
{
	t_stack	a;
	t_node	*current;
	t_node	*start;

	if (ac < 2)
		return (write(2, "Error\n", 6));
	a = parsing(&ac, av, 1);
	
	if (!a.head)
		return (0);
	current = a.head;
	start = a.head;
	while (1)
	{
		printf("%d ", current->value);
		current = current->next;
		if (current == start)
			break ;
	}
	printf("\n");
	return (0);
}
