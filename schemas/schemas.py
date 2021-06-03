

class Gene:
    id: int
    symbol: str
    description: str
    cluster_id: int

    def __init__(self, id: int, symbol: str, description: str, cluster_id: int) -> None:
        self.id = id
        self.symbol = symbol
        self.description = description
        self.cluster_id = cluster_id


class GeneInteraction:
    id: int
    gene1: Gene
    gene2: Gene

    def __init__(self, id, gene1: Gene, gene2: Gene) -> None:
        self.id = id
        self.gene1 = gene1
        self.gene2 = gene2


class Drug:
    id: int
    symbol: str

    def __init__(self, id: int, symbol: str) -> None:
        self.id = id
        self.symbol = symbol


class GeneDrugInteraction:
    id: int
    gene: Gene
    drug: Drug

    def __init__(self, id: int, gene: Gene, drug: Drug) -> None:
        self.id = id
        self.gene = gene
        self.drug = drug
