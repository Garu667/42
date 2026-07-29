/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 17:40:07 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/18 17:11:58 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dst, const void *src, size_t len)
{
	size_t	i;
	char	*tmp_dst;
	char	*tmp_src;

	i = -1;
	tmp_dst = (char *)dst;
	tmp_src = (char *)src;
	if (!src && !dst)
		return (NULL);
	while (++i < len)
		tmp_dst[i] = tmp_src[i];
	return (dst);
}
