#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <sys/time.h>
# include <unistd.h>
# include <stdlib.h>
# include <stdio.h>
# include <string.h>

/* ─── Constantes ─────────────────────────────────────────────── */

# define SCHEDULER_FIFO 0
# define SCHEDULER_EDF  1

/* ─── Forward declarations ───────────────────────────────────── */

typedef struct s_sim    t_sim;
typedef struct s_dongle t_dongle;
typedef struct s_coder  t_coder;
typedef struct s_waiter t_waiter;

/* ─────────────────────────────────────────────────────────────
**  t_waiter — un coder qui attend dans la file d'un dongle
**
**  Quand un coder veut un dongle qui n'est pas libre,
**  il crée un t_waiter et se met dans la file d'attente
**  du dongle. C'est cette structure qui permet FIFO et EDF.
** ───────────────────────────────────────────────────────────── */
typedef struct s_waiter
{
    int             coder_id;     // qui attend
    long            arrived_at;   // timestamp d'arrivée (pour FIFO)
    long            deadline;     // last_compile_start + time_to_burnout (pour EDF)
    pthread_cond_t  ready;        // le dongle signale ce coder via ce cond
    int             granted;      // 1 = le dongle lui a été accordé
}   t_waiter;

/* ─────────────────────────────────────────────────────────────
**  t_dongle — un dongle USB
**
**  Chaque dongle a son propre mutex pour être thread-safe.
**  La file d'attente (heap) contient les t_waiter qui
**  veulent ce dongle, triés selon le scheduler choisi.
** ───────────────────────────────────────────────────────────── */
typedef struct s_dongle
{
    int             id;           // numéro du dongle (0 à n-1)
    pthread_mutex_t mutex;        // protège tout ce struct
    int             in_use;       // 1 = quelqu'un le tient
    long            released_at;  // timestamp de libération (pour le cooldown)

    // File d'attente (heap min — priorité FIFO ou EDF)
    t_waiter        **queue;      // tableau de pointeurs vers les waiters
    int             queue_size;   // nombre de waiters actuellement dans la file
    int             queue_cap;    // capacité allouée du tableau
}   t_dongle;

/* ─────────────────────────────────────────────────────────────
**  t_coder — un coder (= un thread)
**
**  Chaque coder a un pointeur vers son dongle gauche et
**  son dongle droit. Dans la disposition circulaire :
**
**      dongle[0]  dongle[1]  dongle[2]
**         |          |          |
**    Coder 1    Coder 2    Coder 3
**         |          |          |
**      dongle[0]  dongle[1]  dongle[2]
**
**  Coder N :  left = dongles[N-1]
**             right = dongles[N % total]
** ───────────────────────────────────────────────────────────── */
typedef struct s_coder
{
    int             id;                 // numéro (1 à n_coders)
    pthread_t       thread;             // le thread POSIX

    t_sim           *sim;               // accès à la simulation globale
    t_dongle        *left;              // dongle gauche
    t_dongle        *right;             // dongle droit

    long            last_compile_start; // timestamp du dernier début de compile
                                        // → mis à jour juste avant "is compiling"
                                        // → utilisé pour calculer le burnout

    long            deadline;           // last_compile_start + time_to_burnout
                                        // → utilisé par EDF pour prioriser

    int             compile_count;      // combien de fois il a compilé
}   t_coder;

/* ─────────────────────────────────────────────────────────────
**  t_sim — la simulation entière
**
**  C'est la structure "racine" passée à tous les threads.
**  Elle contient les paramètres, les ressources, et l'état.
** ───────────────────────────────────────────────────────────── */
typedef struct s_sim
{
    /* Paramètres (lus depuis argv, jamais modifiés ensuite) */
    int             n_coders;
    long            time_to_burnout;
    long            time_to_compile;
    long            time_to_debug;
    long            time_to_refactor;
    int             n_compiles_required;
    long            dongle_cooldown;
    int             scheduler;           // SCHEDULER_FIFO ou SCHEDULER_EDF

    /* Ressources partagées */
    t_dongle        *dongles;            // tableau de n_coders dongles
    t_coder         *coders;            // tableau de n_coders coders

    /* Horodatage de départ (pour get_elapsed_ms) */
    long            sim_start;

    /* État global de la simulation */
    int             stop;               // 1 = tout le monde doit s'arrêter
    pthread_mutex_t stop_mutex;         // protège stop

    /* Logging thread-safe */
    pthread_mutex_t log_mutex;          // protège printf/write

    /* Thread moniteur */
    pthread_t       monitor;
}   t_sim;

/* ─── Prototypes utils.c ─────────────────────────────────────── */

long    get_time_ms(void);
long    get_elapsed_ms(t_sim *sim);
void    ft_msleep(long ms);
int     is_valid_number(const char *str);
long    parse_positive_long(const char *str);
int     is_valid_scheduler(const char *str);
int     sim_should_stop(t_sim *sim);
int     all_coders_done(t_sim *sim);

#endif
