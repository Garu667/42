unsigned int	ft_strlen(char *str)
{
	unsigned int	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

unsigned int	ft_strlcat(char *dest, char *src, unsigned int size)
{
	unsigned int	i;
	unsigned int	j;
	unsigned int	len_dest;
	unsigned int	len_src;

	j = 0;
	i = ft_strlen(dest);
	len_src = ft_strlen(src);
	len_dest = ft_strlen(dest);
	if (size < 1)
		return (len_src + size);
	while (src[j] && i < (size - 1))
	{
		dest[i + j] = src[j];
		j++;
	}
	dest[i + j] = 0;
	if (size < len_dest)
		return (len_src + size);
	return (len_src + len_dest);
}
