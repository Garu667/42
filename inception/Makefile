.PHONY: all build up down clean fclean re logs ps

# Nom du projet
NAME = inception

# Répertoires
SRCS_DIR = srcs
DATA_DIR = /home/$(USER)/data

# Fichier docker-compose
COMPOSE_FILE = $(SRCS_DIR)/docker-compose.yml

# Couleurs pour les messages
GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[0;33m
NC = \033[0m # No Color

all: build up

# Créer les répertoires de données si nécessaire
create-dirs:
	@echo "$(YELLOW)Création des répertoires de données...$(NC)"
	@mkdir -p $(DATA_DIR)/mysql
	@mkdir -p $(DATA_DIR)/wordpress
	@echo "$(GREEN)Répertoires créés !$(NC)"

# Construire les images Docker
build: create-dirs
	@echo "$(YELLOW)Construction des images Docker...$(NC)"
	@docker-compose -f $(COMPOSE_FILE) build
	@echo "$(GREEN)Images construites avec succès !$(NC)"

# Démarrer les conteneurs
up: create-dirs
	@echo "$(YELLOW)Démarrage des conteneurs...$(NC)"
	@docker-compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)Conteneurs démarrés !$(NC)"
	@echo "$(GREEN)Accédez à votre site sur : https://$(USER).42.fr$(NC)"

# Arrêter les conteneurs
down:
	@echo "$(YELLOW)Arrêt des conteneurs...$(NC)"
	@docker-compose -f $(COMPOSE_FILE) down
	@echo "$(GREEN)Conteneurs arrêtés !$(NC)"

# Voir les logs
logs:
	@docker-compose -f $(COMPOSE_FILE) logs -f

# Voir l'état des conteneurs
ps:
	@docker-compose -f $(COMPOSE_FILE) ps

# Nettoyer (conteneurs + volumes Docker)
clean: down
	@echo "$(YELLOW)Nettoyage des conteneurs et volumes...$(NC)"
	@docker-compose -f $(COMPOSE_FILE) down -v
	@echo "$(GREEN)Nettoyage terminé !$(NC)"

# Nettoyer complètement (+ images + données)
fclean: clean
	@echo "$(RED)Suppression des images et des données...$(NC)"
	@docker system prune -af
	@sudo rm -rf $(DATA_DIR)/mysql/*
	@sudo rm -rf $(DATA_DIR)/wordpress/*
	@echo "$(GREEN)Nettoyage complet terminé !$(NC)"

# Reconstruire tout
re: fclean all

# Aide
help:
	@echo "$(GREEN)Commandes disponibles :$(NC)"
	@echo "  make build    - Construire les images Docker"
	@echo "  make up       - Démarrer les conteneurs"
	@echo "  make down     - Arrêter les conteneurs"
	@echo "  make logs     - Voir les logs en temps réel"
	@echo "  make ps       - Voir l'état des conteneurs"
	@echo "  make clean    - Arrêter et supprimer les volumes"
	@echo "  make fclean   - Nettoyage complet (images + données)"
	@echo "  make re       - Reconstruire tout depuis zéro"
