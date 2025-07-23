import streamlit as st
import random
from collections import Counter

def parse_decklist(deck_text):
    deck = []
    for line in deck_text.strip().split('\n'):
        if not line.strip():
            continue
        try:
            count, name = line.strip().split(' ', 1)
            deck.extend([name] * int(count))
        except ValueError:
            st.error(f"Invalid decklist line: '{line}'")
    return deck

def simulate_hand(deck, hand_size=7):
    return random.sample(deck, hand_size)

def is_keepable(hand, min_lands, max_lands, land_names):
    lands = sum(1 for card in hand if any(land in card for land in land_names))
    return min_lands <= lands <= max_lands

def has_combo(cards, combo_cards):
    return all(any(combo_card in card for card in cards) for combo_card in combo_cards)

def run_simulation(deck, min_lands, max_lands, land_names, combo_cards, combo_in_first_x, trials):
    keepable_count = 0
    combo_hit_count = 0

    for _ in range(trials):
        shuffled = random.sample(deck, len(deck))
        hand = shuffled[:7]
        first_x = shuffled[:combo_in_first_x]

        if is_keepable(hand, min_lands, max_lands, land_names):
            keepable_count += 1

        if has_combo(first_x, combo_cards):
            combo_hit_count += 1

    return keepable_count / trials, combo_hit_count / trials

st.title("MTG Hand Simulator")

st.sidebar.header("Simulation Settings")
deck_input = st.sidebar.text_area("Decklist", height=300, help="Enter your decklist in the format: '4 Lightning Bolt'")

min_lands = st.sidebar.slider("Min Lands in Keepable Hand", 0, 7, 2)
max_lands = st.sidebar.slider("Max Lands in Keepable Hand", 0, 7, 4)
land_names = st.sidebar.text_input("Land Card Names (comma separated)", "Mountain")

combo_card_input = st.sidebar.text_input("Combo Card Names (comma separated)", "Card A, Card B")
combo_in_first_x = st.sidebar.slider("Look for Combo in First X Cards", 1, 20, 7)

trials = st.sidebar.number_input("Number of Simulations", 100, 100000, 10000, step=100)

if st.sidebar.button("Run Simulation"):
    land_keywords = [name.strip() for name in land_names.split(',') if name.strip()]
    combo_cards = [name.strip() for name in combo_card_input.split(',') if name.strip()]
    deck = parse_decklist(deck_input)

    if len(deck) < 7:
        st.error("Deck must contain at least 7 cards.")
    else:
        keep_rate, combo_rate = run_simulation(deck, min_lands, max_lands, land_keywords, combo_cards, combo_in_first_x, trials)
        st.success(f"Keepable Hands: {keep_rate:.2%} over {trials} simulations")
        st.info(f"Combo Present in First {combo_in_first_x} Cards: {combo_rate:.2%}")
