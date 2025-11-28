import streamlit as st
import itertools
import random
import re
import pandas as pd
from io import StringIO
import math

def valider_fichier_sequences(uploaded_file):
    """
    Valide le format du fichier de séquences
    Retourne (valid, positions, error_message)
    """
    try:
        # Lire le fichier ligne par ligne
        content = uploaded_file.getvalue().decode('utf-8')
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Vérification 1: Nombre de lignes
        if len(lines) == 0:
            return False, "❌ Empty file"
        # Vérification 2: Format de chaque ligne
        positions = []
        acides_amines_valides = set('ACDEFGHIKLMNPQRSTVWY')  # 20 acides aminés standards
        
        for i, line in enumerate(lines, 1):
            line = re.findall(r"[A-Za-z0-9]+","".join(line))
            aa_list = [aa.strip().upper() for aa in line]
            if len(aa_list) == 0:
                return False, f"❌ Line {i}: No amino acid found"
            # Vérifier que ce sont bien des acides aminés valides (1 lettre)
            for aa in aa_list:
                if len(aa) != 1:
                    return False, f"❌ Line {i}: '{aa}' is not an amino acid valid (1 letter required only)"
                if aa not in acides_amines_valides:
                    return False, f"❌ Line {i}: '{aa}' is not an amino acid"
            
            # Vérifier qu'il n'y a pas de doublons dans la même position
            if len(aa_list) != len(set(aa_list)):
                return False, f"❌ Line {i}: Duplicates for the same position "
            positions.append(aa_list)        
        return True,"✅ Valid file"
    except Exception as e:
        return False, f"❌ Error reading the file: {str(e)}"

def calcul_total(listes):
    """Calcule le nombre total de sequences possibles"""
    total = 1
    for pos in listes:
        total *= len(pos)
    return total
    print(total)

def generer_aleatoires(n,listes):
    """Génère n sequences aléatoires uniques - VERSION RAPIDE"""
    sequences = set()
    max_attempts = n * 10  # Pour éviter une boucle infinie si n est proche du total
    attempts = 0
    
    while len(sequences) < n and attempts < max_attempts:
        seq = ''.join(random.choice(pos) for pos in listes)
        sequences.add(seq)
        attempts += 1
    
    return sorted(list(sequences))

def generer_premieres(n,listes):
    """Génère les n premières sequences - VERSION RAPIDE"""
    sequences = []
    
    # Calculer les multiplicateurs pour chaque position
    multipliers = [1]
    for i in range(len(listes) - 1, 0, -1):
        multipliers.insert(0, multipliers[0] * len(listes[i]))
    
    # Générer directement la n-ième sequence sans itérer sur toutes les précédentes
    for index in range(n):
        seq = []
        remaining = index
        for pos_idx, mult in enumerate(multipliers):
            choice_idx = remaining // mult
            seq.append(listes[pos_idx][choice_idx])
            remaining = remaining % mult
        sequences.append(''.join(seq))
    
    return sequences

def match_motif(seq, motif):
    """Vérifie si une séquence correspond à un motif (avec - comme wildcard)"""
    if len(motif) != len(seq):
        return False
    for s, m in zip(seq, motif):
        if m != '-' and s != m:
            return False
    return True

def match_regex_motif(seq, pattern):
    """Vérifie si une séquence contient un motif regex (* = n'importe quelle sous-séquence)"""
    # Convertir le pattern utilisateur en regex Python
    # * devient .*
    regex_pattern = pattern.replace('*', '.*')
    return re.search(regex_pattern, seq) is not None

def chercher_motif(motif, max_results,listes):
    """Cherche des sequences correspondant à un motif - VERSION RAPIDE"""
    sequences = []
    
    # Si le motif est juste des underscores, générer aléatoirement
    if motif == "-" * len(listes):
        return generer_aleatoires(max_results)
    
    # Identifier les listes fixes et leurs valeurs
    fixed_listes = []
    variable_listes = []
    
    for i, char in enumerate(motif):
        if char != '-':
            # Vérifier que le caractère est valide pour cette position
            if char in listes[i]:
                fixed_listes.append((i, char))
            else:
                return []  # Motif impossible
        else:
            variable_listes.append(i)
    
    # Si toutes les listes sont fixes, retourner directement
    if not variable_listes:
        return [motif]
    
    # Générer seulement les combinaisons possibles pour les listes variables
    variable_choices = [listes[i] for i in variable_listes]
    
    for combo in itertools.product(*variable_choices):
        if len(sequences) >= max_results:
            break
        
        # Construire la sequence
        seq = list(motif)
        for var_idx, pos_idx in enumerate(variable_listes):
            seq[pos_idx] = combo[var_idx]
        
        sequences.append(''.join(seq))
    
    return sequences

def chercher_regex_motif(pattern, max_results,listes):
    """Cherche des séquences correspondant à un motif regex (* = wildcard)"""
    import re
    sequences = []
    
    # Convertir le pattern utilisateur en regex Python
    regex_pattern = pattern.replace('*', '.*')
    
    # Parcourir toutes les séquences possibles (peut être lent!)
    # On utilise un générateur pour arrêter dès qu'on a assez de résultats
    for seq in itertools.product(*listes):
        if len(sequences) >= max_results:
            break
        
        seq_str = ''.join(seq)
        if re.search(regex_pattern, seq_str):
            sequences.append(seq_str)
    
    return sequences

def calculer_proprietes(seq):
    """Calcule quelques propriétés basiques de la sequence"""
    # Propriétés basiques
    hydrophobic = sum(1 for aa in seq if aa in ['A', 'L', 'P','V','I'])
    charged = sum(1 for aa in seq if aa in ['D', 'E', 'K', 'R','H'])
    polar = sum(1 for aa in seq if aa in ['S','T','N','Q','E','D','K','R','H'])
    
    return {
        'Hydrophobics': hydrophobic,
        'Charged': charged,
        'Polars': polar,
        'Glycines': seq.count('G')
    }

def highlight_motif(sequence: str, motif: str) -> str:
    result = []
    for aa, m in zip(sequence, motif):
        if m != '-':  # position du motif
            result.append(f"<span style='color:red; font-weight:bold'>{aa}</span>")
        else:
            result.append(aa)
    return "".join(result)

def highlight_motif_regex(sequence: str, pattern: str) -> str:
    """Colore uniquement les lettres fixes du pattern selon le regex"""
    # Convertir le pattern en regex
    regex_pattern = pattern.replace('*', '.*')
    
    match = re.search(regex_pattern, sequence)
    if not match:
        return sequence
    
    matched_part = match.group()
    match_start = match.start()
    
    # Extraire les segments fixes (entre les *)
    fixed_segments = [seg for seg in pattern.split('*') if seg]
    
    if not fixed_segments:
        return sequence
    
    # Trouver chaque segment dans le match
    positions_to_color = []
    search_from = 0
    
    for segment in fixed_segments:
        pos = matched_part.find(segment, search_from)
        if pos != -1:
            # Ajouter toutes les positions du segment
            for i in range(len(segment)):
                absolute_pos = match_start + pos + i
                positions_to_color.append(absolute_pos)
            search_from = pos + len(segment)
    
    # Construire le résultat
    result = ""
    last_pos = 0
    
    for pos in sorted(set(positions_to_color)):
        result += sequence[last_pos:pos]
        result += f"<span style='color:red; font-weight:bold'>{sequence[pos]}</span>"
        last_pos = pos + 1
    
    result += sequence[last_pos:]
    
    return result
