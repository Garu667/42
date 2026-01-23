# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: quentin <quentin@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/12 18:08:48 by ramaroud          #+#    #+#              #
#    Updated: 2026/01/22 18:47:12 by quentin          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME        = push_swap
BONUS_NAME  = checker

OBJDIR = objs

CC = gcc
CFLAGS = -Wall -Werror -Wextra -MMD -MP

MANDATORY_SRCS	= algo_utils.c			\
				benchmark.c				\
				check.c 				\
				chunk_sort.c 			\
				ft_op.c 				\
				ft_split.c 				\
				index.c 				\
				main_push_swap.c		\
				parsing.c 				\
				push_op.c		 		\
				radix_sort.c 			\
				reverse_op.c 			\
				rotate_op.c 			\
				selection_sort.c 		\
				swap_op.c 				\
				tiny_sort.c				\
				utils.c					\
				utils2.c

BONUS_SRCS		= bonus/main_checker.c 		\
				bonus/gnl.c 				\
				bonus/gnl_utils.c			\
				check.c 					\
				ft_split.c 					\
				parsing.c 					\
				push_op.c		 			\
				reverse_op.c 				\
				rotate_op.c 				\
				swap_op.c 					\
				utils.c						\
				utils2.c

MANDATORY_OBJS = $(MANDATORY_SRCS:%.c=$(OBJDIR)/%.o)
BONUS_OBJS = $(BONUS_SRCS:%.c=$(OBJDIR)/%.o)

DEPS = $(OBJS:.o=.d) $(BONUS_OBJS:.o=.d)

all: $(NAME)

$(NAME): $(MANDATORY_OBJS)
	$(CC) $(CFLAGS) $(MANDATORY_OBJS) -o $(NAME) 

bonus: $(BONUS_NAME)

$(BONUS_NAME): $(BONUS_OBJS)
	$(CC) $(CFLAGS) $(OBJS) $(BONUS_OBJS) -o $(BONUS_NAME)

$(OBJDIR)/%.o: %.c
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(OBJDIR)

fclean: clean
	rm -f $(NAME) $(BONUS_NAME)

re: fclean all

-include $(DEPS)

.PHONY: all clean fclean re bonus
