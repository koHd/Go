Love the focus — now that your core Go engine is working beautifully, here’s a curated list of the **next best features** to add. These are ranked by **impact vs effort**, based on where your project is now:

---

## 🧩 Essential Gameplay Features

### 1. 🕊️ **Pass Turn Handling** (HIGH IMPACT — LOW EFFORT)
- Add key (e.g. `p`) to pass your turn
- Track if **two consecutive passes** happen → end the game

➡️ **This is the official way to finish a Go game**

---

### 2. 🧮 **Scoring System** (HIGH IMPACT — MODERATE EFFORT)
- Count each player’s:
  - ✅ Captured stones (already possible)
  - ✅ Territory (empty points surrounded)
- Add **Komi** to White
- Show score at game end

---

### 3. 📜 **Move Log / History** (MEDIUM IMPACT — LOW EFFORT)
- Store each move as a list: `(player, index)`
- Could later be used to:
  - Undo moves
  - Replay moves
  - Export game records

---

### 4. 🏁 **End Game Summary Screen** (MEDIUM IMPACT — LOW EFFORT)
- When the game ends (after 2 passes), show:
  - Captures
  - Territory count
  - Final score
  - Winner

---

## 🎨 TUI/UX Enhancements

### 5. 🔠 **Coordinate Labels (A–I / 1–9)** (MEDIUM EFFORT — HIGH POLISH)
- Add row/column headers to your board
- Helps with strategy & move references

---

### 6. 🌟 **Highlight Last Move** (LOW EFFORT — HIGH POLISH)
- Store index of last placed stone
- Highlight it in the draw loop (e.g. with `*` or color)

---

### 7. 🔁 **"Play Again" Prompt** (LOW EFFORT — MEDIUM VALUE)
- Let players restart after game end
- Useful for casual sessions

---

### 8. 🎨 **Use Curses Colors** (LOW EFFORT — COSMETIC)
- Make black stones truly black
- Color error messages (e.g., red for “Illegal move”)

---

## 🧠 Advanced Strategy Features (Optional for Later)

- 🔬 AI opponent (random / rule-based)
- 🧪 Dead stone marking at end (for scoring help)
- 💾 Save/Load game state

---

## 🧭 Suggested Next Steps

If you’re up for it, this would be a perfect next mini-milestone:

> ✅ **Add pass handling** →  
> ✅ **Trigger game end after 2 passes** →  
> ✅ **Show a game over summary screen with fake scoring (for now)**

Then we can work together to implement real territory counting logic.

Want to start with **pass turn support + game end detection**? It’s a super clean and rewarding addition.
