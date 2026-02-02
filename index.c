/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   index.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/01 12:32:35 by ramaroud          #+#    #+#             */
/*   Updated: 2026/02/01 12:32:35 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

static int	define_index(int *array, int size, int value)
{
	int	i;

	i = 0;
	while (i < size)
	{
		if (array[i] == value)
			return (i);
		i++;
	}
	return (-1);
}

static void	bubble_sort_array(int *array, int size)
{
	int	i;
	int	j;
	int	tmp;

	i = 0;
	while (i < size - 1)
	{
		j = i + 1;
		while (j < size)
		{
			if (array[i] > array[j])
			{
				tmp = array[i];
				array[i] = array[j];
				array[j] = tmp;
			}
			j++;
		}
		i++;
	}
}

static int	*stack_to_array(t_stack *a)
{
	int		*array;
	t_node	*current;
	int		i;

	array = malloc(sizeof(int) * a->size);
	if (!array)
		return (NULL);
	current = a->head;
	i = 0;
	while (i < a->size)
	{
		array[i] = current->value;
		current = current->next;
		i++;
	}
	return (array);
}

void	stack_to_index(t_stack *a)
{
	int		*array;
	t_node	*current;
	int		i;

	if (!a || a->size <= 0 || !a->head)
		return ;
	array = stack_to_array(a);
	if (!array)
		return ;
	bubble_sort_array(array, a->size);
	current = a->head;
	i = 0;
	while (i < a->size)
	{
		current->index = define_index(array, a->size, current->value);
		current = current->next;
		i++;
	}
	free(array);
}
