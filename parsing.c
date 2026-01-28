/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: qgairaud <qgairaud@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 16:02:44 by ramaroud          #+#    #+#             */
/*   Updated: 2026/01/28 17:46:17 by qgairaud         ###   ########.fr       */
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
	new_node->prev = NULL;
	return (new_node);
}

static void	add_node_back(t_stack *stack, t_node *new_node)
{
	t_node	*current;

	if (!stack->head)
	{
		stack->head = new_node;
		new_node->next = new_node;
		new_node->prev = new_node;
	}
	else
	{
		current = stack->head->prev;
		current->next = new_node;
		new_node->prev = current;
		new_node->next = stack->head;
		stack->head->prev = new_node;
	}
	stack->size++;
}

static int	parse_multiple(char **split, t_stack *a)
{
	t_node	*new_node;
	int		value;
	int		count;
	int		i;

	i = 0;
	count = 0;
	while (split[count])
		count++;
	if (count == 0)
		return (0);
	while (i < count)
	{
		if (ft_atoi(split[i], &value) <= 0
			|| !(value <= INT_MAX && value >= INT_MIN) || is_double(a, value))
			return (1);
		new_node = create_node(value);
		if (!new_node)
			return (1);
		add_node_back(a, new_node);
		i++;
	}
	return (0);
}

int	parsing(t_stack *a, int ac, char **av)
{
	char	**split;
	int		count;
	int		i;

	i = 0;
	while (av[ac - 1][0] == '-' && av[ac - 1][1] == '-')
		ac--;
	while (++i < ac)
	{
		count = 0;
		while (av[i][0] == '-' && av[i][1] == '-')
			i++;
		split = ft_split(av[i], ' ');
		if (!split)
			return (1);
		while (split[count])
			count++;
		if (parse_multiple(split, a))
			return (free_all(a, split));
		free_split(split, 0, 3);
	}
	return (0);
}
