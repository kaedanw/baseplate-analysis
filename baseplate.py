from math import cos, sin, radians


def main():
    # Bolts Setup:
    pcd = 460
    col = 219
    nbolts = 6
    B = Bolts(pcd, col, nbolts)

    # Calculations Setup:
    # Allow user to perform calculations from offset position
    # (CHOICES ONLY: 0 OR theta/2)
    roadOffsetDegree = 0

    Mu = 53
    Vu = 10
    analyseT(B, Mu, Vu)
    B.display()


def analyseT(bolts, Mu, Vu):
    Gy = bolts.Gy
    Gx = bolts.Gx

    L2y = sum(L**2 for L in Gy)
    L2x = sum(L**2 for L in Gx)

    for bolt in bolts.bolts:
        # Tbolt* = M* x Lbolt / (L1^2 + L2^2 + L3^2 + ...)
        bolt.Ty = round(((Mu * 1E6 * bolt.Ly) / L2y * 1E-3) + (Vu / bolts.nbolts), 2) if bolt.Ly >= 0 else 0
        bolt.Tx = round(((Mu * 1E6 * bolt.Lx) / L2x * 1E-3) + (Vu / bolts.nbolts), 2) if bolt.Lx >= 0 else 0   


class Bolts:
    def __init__(self, pcd, col, nbolts):
        self.pcd = pcd
        self.col = col
        self.nbolts = nbolts

        self.r = self.pcd / 2
        self.c = self.col / 2
        self.theta = 360 / self.nbolts
        self.threshold = -self.c
        
        self.bolts = self.createBolts()
        self.Gy, self.Gx = self.createBoltGroups() # to implement orientation degree variation

    def createBolts(self):
        bolts = []
        degree = 90 # Initial starting bolt position, Always calculated from top
        for _ in range(self.nbolts):
            bolts.append(self.Bolt(self, degree))
            degree -= self.theta
        return sorted(bolts, key=lambda bolt: bolt.y, reverse=True)

    def display(self):
        for bolt in self.bolts:
            bolt.display()

    def createBoltGroups(self):
        Gy = {}
        Gx = {}
        
        for bolt in self.bolts:
            Ly = round(bolt.y + self.c, 2) if bolt.y > self.threshold else -1
            Lx = round(bolt.x + self.c, 2) if bolt.x > self.threshold else -1

            if Ly >= 0:
                if Ly not in Gy:
                    Gy[Ly] = 1
                else:
                    Gy[Ly] += 1

            if Lx >= 0:
                if Lx not in Gx:
                    Gx[Lx] = 1
                else:
                    Gx[Lx] += 1

            bolt.Ly = Ly
            bolt.Lx = Lx
            
        Gy = {k:Gy[k] for k in sorted(Gy, reverse=True)}
        Gx = {k:Gx[k] for k in sorted(Gx, reverse=True)}

        return Gy, Gx

    def displayBoltGroups(self, Gy, Gx):
        print("Gy")
        print(Gy)
        for L, l in Gy.items():
            print(L, l)

        print("Gx")
        print(Gx)
        for L, l in Gx.items():
            print(L, l)

    class Bolt:
        boltId = 1

        def __init__(self, bolts, degree):
            self.id = type(self).boltId
            self.x = round(bolts.r * cos(radians(degree)), 2)
            self.y = round(bolts.r * sin(radians(degree)), 2)
            type(self).boltId += 1

        def display(self):
            print(*(f"{k}: {v:>7}" for k,v in self.__dict__.items()), sep=', ')


if __name__ == "__main__":
    main()