/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 13:13:34 by ramaroud          #+#    #+#             */
/*   Updated: 2025/11/25 13:16:59 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H
# include <stdarg.h>
# include <unistd.h>

int	ft_putchar(char c);
int	ft_putstr(char *str);
int	ft_putnbr(unsigned int n);
int	ft_putnbr_base(int nbr, char *base);
int	ft_putnbr_base2(unsigned int nbr, char *base);
int	ft_putnbr_base3(unsigned long long int nbr);
int	format(const char *str, va_list args);
int	ft_printf(const char *str, ...)__attribute__((format(printf, 1, 2)));

#endif
