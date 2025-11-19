/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 15:44:23 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/13 13:27:09 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dst, const void *src, size_t len)
{
	char	*tmp_dst;
	char	*tmp_src;
	size_t	i;

	i = -1;
	if (!src && !dst)
		return (NULL);
	tmp_dst = (char *)dst;
	tmp_src = (char *)src;
	if (tmp_dst > tmp_src)
		while (len--)
			tmp_dst[len] = tmp_src[len];
	else
	{
		while (++i < len)
			tmp_dst[i] = tmp_src[i];
	}
	return (dst);
}
/*
int	main(int ac, char **av)
{
	char	str1[] = "abcde";
	char	str2[] = "salut";
	printf("%s\n", (char *)ft_memmove((void *)str1, (const void *)str2, 3));

	char	str3[] = "abcde";
	char	str4[] = "salut";
	printf("%s\n", (char *)memmove((void *)str3, (const void *)str4, 3));
}
*/
