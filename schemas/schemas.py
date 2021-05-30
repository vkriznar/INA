

class Gene:
    id: int
    symbol: str
    description: str

    def __init__(self, id, symbol, description) -> None:
        self.id = id
        self.symbol = symbol
        self.description = description


class GeneInteraction:
    id: int
    gene1: Gene
    gene2: Gene

    def __init__(self, id, gene1, gene2) -> None:
        self.id = id
        self.gene1 = gene1
        self.gene2 = gene2
