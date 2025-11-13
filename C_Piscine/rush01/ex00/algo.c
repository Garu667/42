/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   algo.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: saidriss <saidriss@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/09/21 22:09:54 by saidriss          #+#    #+#             */
/*   Updated: 2024/09/21 22:24:32 by saidriss         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdio.h>

int	already_here(int grid[4][4], int row, int col, int num)
{
	int	i;

	i = 0;
	while (i < 4)
	{
		if (grid[row][i] == num || grid[i][col] == num)
			return (0);
		i++;
	}
	return (1);
}

void ft_zero(int *i, int *j, int *k)
{
  *i = 0;
  *j = 0;
  *k = 0;
}

int	check_col(int grid[4][4], int *constraints, int x)
{
	int	i;
	int	max;
	int	visible;

  ft_zero(&i, &max, &visible);
	while (i < 4)
	{
		if (grid[i++][x] > max)
		{
			max = grid[i][x];
			visible++;
		}
	}
	max = 0;
	while (i > 0)
	{
		if (grid[i - 1][x] > max)
		{
			max = grid[i - 1][x];
			visible++;
		}
		i--;
	}
	return ((visible - (constraints[x] + constraints[x + 4])));
}

int	check_row(int grid[4][4], int *constraints, int y)
{
	int	i;
	int	max;
	int	visible;

  ft_zero(&i, &max, &visible);
	while (i < 4)
	{
		if (grid[y][i++] > max)
		{
			max = grid[y][i];
			visible++;
		}
	}
	max = 0;
	while (i >= 0)
	{
		if (grid[y][i - 1] > max)
		{
			max = grid[y][i - 1];
			visible++;
		}
		i--;
	}
  printf("%d\t", visible);
	return ((visible - (constraints[y + 8] + constraints[y + 12])));
}

int	check_all(int grid[4][4], int *constraints)
{
	int	i;
	int	line[4];

	i = 0;
	while (i < 4)
	{
		if (check_col(grid, constraints, i) != 0)
			return (0);
		i++;
	}
	i = 0;
	while (i < 4)
	{
		if (check_row(grid, constraints, i) != 0)
			return (0);
		i++;
	}
	return (1);
}

int	solve_puzzle(int grid[4][4], int *constraints, int row, int col)
{
	int	num;

	num = 1;
	if (row == 4)
		return (check_all(grid, constraints));
	if (col == 4)
		return (solve_puzzle(grid, constraints, row + 1, 0));
	while (num <= 4)
	{
		if (already_here(grid, row, col, num))
		{
			grid[row][col] = num;
			if (solve_puzzle(grid, constraints, row, col + 1))
				return (1);
			grid[row][col] = 0;
		}
		num++;
	}
	return (0);
}
