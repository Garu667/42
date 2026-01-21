# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: quentin <quentin@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/12 18:08:48 by ramaroud          #+#    #+#              #
#    Updated: 2026/01/21 12:45:40 by quentin          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

SRCS	= check.c		\
		ft_op.c			\
		index.c			\
		utils.c			\
		utils2.c		\
		parsing.c		\
		swap_op.c		\
		push_op.c		\
		ft_split.c		\
		benchmark.c		\
		rotate_op.c		\
		tiny_sort.c		\
		chunk_sort.c	\
		algo_utils.c	\
		radix_sort.c	\
		reverse_op.c	\
		select_sort.c	\
		main_push_swap.c
OBJS	= $(SRCS:.c=.o)

BONUS	= bonus/gnl.c		\
		check.c				\
		utils.c				\
		utils2.c			\
		parsing.c			\
		swap_op.c			\
		push_op.c			\
		ft_split.c			\
		rotate_op.c			\
		reverse_op.c		\
		bonus/gnl_utils.c	\
		bonus/main_checker.c
BONUS_OBJS = $(BONUS:.c=.o)

CC				= cc
RM				= rm -f
CFLAGS			= #-Wall -Wextra -Werror
SRC_INCLUDES	= header.h
NAME			= push_swap
BONUS_NAME		= checker

all:		$(NAME)

$(NAME):	$(OBJS)
			$(CC) $(OBJS) -o $(NAME) 

clean:
			$(RM) $(OBJS) $(BONUS_OBJS)

fclean:		clean
			$(RM) $(NAME) $(BONUS_NAME) .bonus

re:		fclean all

bonus:	.bonus

.bonus:		$(BONUS_OBJS)
			$(CC) $(BONUS_OBJS) -o $(BONUS_NAME)
			touch .bonus

%.o:		%.c header.h
			$(CC) $(CFLAGS) -c $< -o $@

.PHONY:		all clean fclean re bonus
