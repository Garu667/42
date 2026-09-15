/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ramaroud <ramaroud@student.42lyon.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/06 08:34:55 by ramaroud          #+#    #+#             */
/*   Updated: 2026/09/15 10:00:00 by ramaroud         ###   ########lyon.fr   */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <sys/time.h>
# include <unistd.h>
# include <stdlib.h>
# include <stdio.h>
# include <string.h>

# define SCHEDULER_FIFO	1
# define SCHEDULER_EDF	2

typedef enum e_error
{
	ERR_ARGC = 1,
	ERR_PARSING,
	ERR_ALLOC_CODERS,
	ERR_ALLOC_DONGLES,
	ERR_ALLOC_QUEUE,
	ERR_THREAD_CREATE
}	t_error;

typedef struct s_sim	t_sim;

typedef struct s_waiter
{
	int		coder_id;
	long	seq;
	long	deadline;
	int		n_compile;
}	t_waiter;

typedef struct s_dongle
{
	int		in_use;
	int		reserved;
	long	released_at;
}	t_dongle;

typedef struct s_coder
{
	int				id;
	pthread_t		thread;
	t_sim			*sim;
	t_dongle		*left;
	t_dongle		*right;
	t_waiter		waiter;
	pthread_cond_t	cond;
	int				granted;
	long			last_compile;
	int				compile_count;
}	t_coder;

typedef struct s_sim
{
	int				n_coders;
	long			time_burnout;
	long			time_compile;
	long			time_debug;
	long			time_refactor;
	int				n_req_compiles;
	long			dongle_cd;
	int				scheduler;
	t_dongle		*dongles;
	t_coder			*coders;
	t_waiter		**queue;
	int				qsize;
	long			seq;
	long			sim_start;
	int				can_start;
	int				stop;
	pthread_mutex_t	sched_mutex;
	pthread_cond_t	sched_cond;
	pthread_mutex_t	stop_mutex;
	pthread_mutex_t	log_mutex;
	pthread_mutex_t	coders_mutex;
	pthread_t		monitor;
	pthread_t		arbiter;
}	t_sim;

/*		parsing.c		*/
int			parsing(char **av, t_sim *sim);
/*		utils.c		*/
long		get_time_ms(void);
void		ft_msleep(long ms, t_sim *sim);
long		get_elapsed_ms(t_sim *sim);
int			all_coders_done(t_sim *sim);
int			sim_should_stop(t_sim *sim);
/*		queue.c		*/
void		queue_push(t_sim *sim, t_waiter *waiter);
void		queue_remove(t_sim *sim, t_waiter *waiter);
/*		init.c		*/
int			init_sim(t_sim *sim);
/*		scheduler.c		*/
void		*sched_routine(void *arg);
void		sched_wait(t_sim *sim);
/*		dongle.c		*/
int			request_dongles(t_coder *coder);
void		release_dongles(t_coder *coder);
/*		coders.c		*/
void		log_action(t_sim *sim, int coder_id, const char *action);
void		*coder_routine(void *arg);
long		coder_status(t_sim *sim, int i, int *done);
/*		error.c		*/
int			free_return(t_sim *sim, int n_free, int ret_flag, int i);
/*		main.c		*/
void		*stop_simulation(t_sim *sim);
void		*monitor_routine(void *arg);
void		start_simulation(t_sim *sim);
void		wait_for_start(t_sim *sim);

#endif
