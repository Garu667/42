#ifndef UTILS_H
# define UTILS_H

# include "codexion.h"  // pour avoir accès à t_sim, t_coder, etc.
#include <stdio.h>
#include <sys/time.h>

/* ─── Temps ─────────────────────────────────────────────────── */

// Retourne le timestamp actuel en millisecondes
// (depuis epoch, via gettimeofday)
long    get_time_ms(void)
{
    struct timeval  tv;

    gettimeofday(&tv, NULL);
    return (tv.tv_sec * 1000L + tv.tv_usec / 1000);
}
// Retourne le temps écoulé depuis le début de la simulation en ms
// Utilise sim->sim_start pour calculer
long	get_elapsed_ms(t_sim *sim)
{
    return (get_time_ms() - sim->sim_start);
    // sim->sim_start est initialisé au tout début du main
}
// Endort le thread courant pendant ms millisecondes
// (wrapper autour de usleep, qui prend des microsecondes)
void    ft_msleep(long ms)
{
    long    start;

    start = get_time_ms();
    while (get_time_ms() - start < ms)
        usleep(100);
}

/* ─── Parsing / Validation ───────────────────────────────────── */

// Vérifie qu'une string ne contient que des chiffres
// Retourne 1 si valide, 0 sinon
int         is_valid_number(const char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		if (str[i] < '0' && str[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

// Convertit une string en long et vérifie qu'elle est > 0
// Retourne la valeur si valide, -1 si invalide
long        parse_positive_long(const char *str);

// Vérifie que le scheduler est "fifo" ou "edf"
// Retourne 1 si valide, 0 sinon
int         is_valid_scheduler(const char *str);

/* ─── Simulation ─────────────────────────────────────────────── */

// Retourne 1 si la simulation doit s'arrêter (stop flag levé)
// Retourne 0 sinon
// (lecture thread-safe via stop_mutex)
int	sim_should_stop(t_sim *sim)
{
	if (sim->stop == 1)
		return (1);
	return (0);
}

// Vérifie si tous les coders ont atteint n_compiles_required
// Retourne 1 si oui, 0 sinon
int         all_coders_done(t_sim *sim)
{
	int required;
	int	compiled;
	int	i;

	i = 0;
	compiled = 0;
	required = sim->n_compiles_required;
	while (i < sim->n_coders)
    {
		compiled = sim->coders[i].compile_count;
		if (compiled < required)
			return (0);
		i++;
    }
	return (1);
}

#endif
