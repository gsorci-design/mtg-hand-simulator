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

def run_simulation(deck, min_lands, max_lands, land_names, trials):
    keepable_count = 0
    for _ in range(trials):
        hand = simulate_hand(deck)
        if is_keepable(hand, min_lands, max_lands, land_names):
            keepable_count += 1
    return keepable_count / trials

st.title("MTG Hand Simulator")

st.sidebar.header("Simulation Settings")
deck_input = st.sidebar.text_area("Decklist", height=300, help="Enter your decklist in the format: '4 Lightning Bolt'")

min_lands = st.sidebar.slider("Min Lands in Keepable Hand", 0, 7, 2)
max_lands = st.sidebar.slider("Max Lands in Keepable Hand", 0, 7, 4)
land_names = st.sidebar.text_input("Land Card Names (comma separated)", "Mountain")
trials = st.sidebar.number_input("Number of Simulations", 100, 100000, 10000, step=100)

if st.sidebar.button("Run Simulation"):
    land_keywords = [name.strip() for name in land_names.split(',') if name.strip()]
    deck = parse_decklist(deck_input)

    if len(deck) < 7:
        st.error("Deck must contain at least 7 cards.")
    else:
        keep_rate = run_simulation(deck, min_lands, max_lands, land_keywords, trials)
        st.success(f"Keepable Hands: {keep_rate:.2%} over {trials} simulations")
