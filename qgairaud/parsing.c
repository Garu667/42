/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:44 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/20 14:16:23 by qgairaud         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

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
	return (new_node);
}

static void	add_node_back(t_stack *stack, t_node *new_node)
{
	t_node	*current;

	if (!stack->head)
		stack->head = new_node;
	else
	{
		current = stack->head;
		while (current->next)
			current = current->next;
		current->next = new_node;
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
		if (!ft_atoi(split[i], &value)
			|| !(value <= INT_MAX && value >= INT_MIN) || is_double(a, value))
			exit(write(2, "Error\n", 6));
		new_node = create_node(value);
		if (!new_node)
			exit(write(2, "Error\n", 6));
		add_node_back(a, new_node);
		i++;
	}
}

t_stack	parsing(int *ac, char **av)
{
	t_stack	a;
	char	**split;
	int		count;
	int		flag;
	int		i;

	i = 0;
	count = 0;
	a.size = 0;
	a.head = NULL;
	flag = ft_check_flag(av, &i);
	if (flag == -1)
		exit(write(2, "Error\n", 6));
	while (++i != (*ac))
	{
		split = ft_split(av[i], ' ');
		if (!split)
			exit(write(2, "Error\n", 6));
		parse_multiple(split, &a);
		free_split(split, count, 2);
	}
	(*ac) = flag;
	return (a);
}
