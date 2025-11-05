# Python in Science Applications

This repository was created to share projects developed for *"Python w Zastosowaniach Naukowych"*,  
which is a course at the **Warsaw University of Technology**, **Faculty of Physics**.

---

## 📑 Table of Contents
1. [Project 1 – Console Histogram of Words](#project-1--console-histogram-of-words)

---

## 📊 Project 1 – Console Histogram of Words

The program [`wordHistogram.py`](Console_Histogram_project01/wordHistogram.py)  
loads a text file, counts the frequency of each word, and displays a histogram of word occurrences using the `ascii_graph` library.

It also accepts several command-line parameters to control how the program operates:

- **`-i`** or **`--input`** – input filename *(required)*  
- **`-hl`** or **`--histlimit`** – number of words to display in the histogram  
- **`-m`** or **`--minimal`** – minimum length of words to include  
- **`-el`** or **`--excludedList`** – list of words to ignore  

At the **Console Histogram** directory, there are two versions of Joseph Conrad's book *"Heart of Darkness"*, obtained from legal public-domain sources:

- 🇬🇧 **English version:** [Project Gutenberg](https://www.gutenberg.org/ebooks/219)  
- 🇵🇱 **Polish version:** [Wolne Lektury](https://wolnelektury.pl/katalog/lektura/conrad-jadro-ciemnosci.html)

These texts are used as sample data for testing and demonstrating the program's functionality.

---

**Example usage:**
```bash
python wordHistogram.py Heart_of_darkness.txt -hl 5 -m 3 -el the
```
---

## 🧠 Technologies Used
- Python 3.12.3  
- `argparse`, `ascii_graph`

---
