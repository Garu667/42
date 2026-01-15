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

#include "../header.h"

int	main(int ac, char **av)
{
	t_stack	a;
	t_node	*current;
	t_node	*start;

	if (ac < 2)
		return (write(2, "Error\n", 6));
	a = parsing(&ac, av);
	
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
