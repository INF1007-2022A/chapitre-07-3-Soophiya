#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mido # pip install mido pour installer la librairie


NOTES_PER_OCTAVE = 12


def build_note_dictionaries(note_names, add_octave_no=True):
	C0_MIDI_NO = 12 # Plus basse note sur les pianos est La 0, mais on va commencer à générer les noms sur Do 0

	midi_to_name = {}
	name_to_midi = {}
	# Pour chaque octave de 0 à 8 (inclus). On va générer tout l'octave 8, même si la dernière note du piano est Do 8
	for octave in range(9):
		
		# Pour chaque note de l'octave
		for note in range(NOTES_PER_OCTAVE):
			
			# Calculer le numéro MIDI de la note et ajouter aux deux dictionnaires
			numero_midi = C0_MIDI_NO + octave * NOTES_PER_OCTAVE + note
			# Ajouter le numéro de l'octave au nom de la note si add_octave_no est vrai
			nom_note = note_names[note] + str(octave) if add_octave_no else note_names[note]
			midi_to_name[numero_midi] = nom_note
			# Garder les numéros de notes dans name_to_midi entre 0 et 11 si add_octave_no est faux
			note_in_octave = note if add_octave_no else note % NOTES_PER_OCTAVE
			name_to_midi[nom_note] = note_in_octave
			
	return midi_to_name, name_to_midi

def build_print_note_name_callback(midi_to_name):
	
	#créer une fonction qui prend en paramètre un message midi et qui affiche le nom de la note correspondante
	#créer et retourner le callback

	def callback(message):
		if message.type == "note_on" and message.velocity > 0:
			print(midi_to_name[message.note])
		return callback

def build_print_chord_name_callback(chord_names_and_notes, name_to_midi):
	# Construire le dictionnaire d'assocations entre état des notes et accord joué.
	cordes = {}

	for nom_accord, notes in chord_names_and_notes.items():
		notes_cordes = [False] * NOTES_PER_OCTAVE
		for note in notes:
			notes_cordes[name_to_midi[note] % NOTES_PER_OCTAVE] = True
		cordes[tuple(notes_cordes)] = nom_accord

	# Créez et retourner le callback
	def callback(message):
		if message.type == "note_on" and message.velocity > 0:
			cordes[message.note] = True
		elif message.type == "note_off" or (message.type == "note_on" and message.velocity == 0):
			cordes[message.note] = False
		else:
			return
		if tuple(cordes) in cordes:
			print(cordes[tuple(cordes)])
		return callback
	

def main():
	PORT_MIDI = "UnPortMIDI 0"

	english_names = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
	solfeggio_names = ["Do", "Réb", "Ré", "Mib", "Mi", "Fa", "Fa#", "Sol", "Lab", "La", "Sib", "Si"]

	midi_to_name_eng_8va, name_to_midi_eng_8va = build_note_dictionaries(english_names, True)
	midi_to_name_fr, name_to_midi_fr = build_note_dictionaries(solfeggio_names, False)
	print(midi_to_name_eng_8va[64])
	print(name_to_midi_eng_8va["C0"])
	print(midi_to_name_fr[61])
	print(midi_to_name_fr[73])
	print(name_to_midi_fr["Fa#"])

	input("Appuyez sur ENTER pour passer à l'étape suivante...")
	print("- - " * 30)
	
	midi_to_name, name_to_midi = build_note_dictionaries(solfeggio_names, True)
	print_note_name = build_print_note_name_callback(midi_to_name)
	keyboard = mido.open_input(PORT_MIDI, callback=print_note_name)

	input("Affichage des noms de notes (Appuyez sur ENTER pour passer à l'étape suivante)..." "\n")
	keyboard.close()

	print("- - " * 30)

	chord_names = {
		"Do majeur" : ("Do", "Mi", "Sol"),
		"Fa majeur" : ("Fa", "La", "Do"),
		"Sol majeur" : ("Sol", "Si", "Ré"),
	}
	
	midi_to_name, name_to_midi = build_note_dictionaries(solfeggio_names, False)
	print_chord_name = build_print_chord_name_callback(chord_names, name_to_midi)
	keyboard = mido.open_input(PORT_MIDI, callback=print_chord_name)
	
	input("Affichage des noms d'accords (Appuyez sur ENTER pour passer à l'étape suivante)..." "\n")
	keyboard.close()

if __name__ == "__main__":
	main()
