*This project has been created as part of the 42 curriculum by* ramaroud.

# get_next_line

## 📝 Description

**get_next_line** est un projet dont l’objectif est d’implémenter une fonction capable de lire un fichier **ligne par ligne**, de manière efficace et sans fuite mémoire.  
La fonction doit retourner **une ligne complète** (terminée par un `\n` ou par la fin du fichier) à **chaque appel**, indépendamment du descripteur de fichier utilisé.

Ce projet introduit plusieurs notions importantes :
- La gestion bas-niveau des fichiers via `read()`
- Les buffers statiques et dynamiques
- La manipulation de chaînes de caractères en C
- La gestion d'un "reste" entre les appels grace aux variables statics 
- La robustesse de la mémoire (malloc/free)

---

## 🚀 Instructions

### 🔧 Compilation

```bash
cc -Wall -Wextra -Werror get_next_line.c get_next_line_utils.c -D BUFFER_SIZE=42
```

## Ressources

`man read`
`man open`
`man close`
[Vidéo explicative](https://youtu.be/-Mt2FdJjVno)
L'ia à été utilisé pour structurer le README
