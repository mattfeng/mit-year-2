def main():
    # read in potential motifs (motif candidates)
    # potential_motifs_conserved.txt
    # potential_motifs_frequent.txt
    motifs = []
    suffix = "conserved"
    with open(f"potential_motifs_{suffix}.txt") as f:
        for line in f:
            motifs.append(line.strip())
    
    # read in known motifs
    known = dict()
    with open("yeast_motifs.txt") as f:
        f.readline()
        for line in f:
            name, motif = line.strip().split(" ")
            known[motif] = name
    
    # compare the two
    for motif in motifs:
        if motif in known:
            print(f"{motif} -> {known[motif]}")


if __name__ == "__main__":
    main()
