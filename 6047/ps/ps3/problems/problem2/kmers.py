from collections import Counter

def main():
    K = 6
    motifs = Counter()
    conserved = Counter()
    seq = open("allinter").read()
    cons = open("allintercons").read()
    print(len(seq), len(cons))

    for i in range(0, len(seq) - K):
        motif = seq[i:i + K]
        if any(char in seq[i:i + K] for char in "-#"):
            continue

        motifs[motif] += 1
        conserved[motif] += cons[i:i + K].count("*")
    
    # normalization of conservation by frequency
    normalized = {}
    for motif, count in conserved.items():
        normalized[motif] = count / K / motifs[motif]

    print("Most common motifs:")
    for motif, count in sorted(list(motifs.items()), key=lambda x: x[1], reverse=True)[:50]:
        print(f"{motif}: {count:>5d} {normalized[motif]:>0.5f}")
    
    print("\nMost conserved motifs:")
    for motif, count in sorted(list(normalized.items()), key=lambda x: x[1], reverse=True)[:50]:
        print(f"{motif}: {count:>0.5f} {motifs[motif]:>5d}")

if __name__ == "__main__":
    main()