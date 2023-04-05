class DisjSet:
    def __init__(self, parent):
        self.parent = parent
        self.rank = {}
        for i in parent:
            self.rank[i]=1
            
 
    def find(self, x):
        if (self.parent[x] != x):
            self.parent[x] = self.find(self.parent[x])
 
        return self.parent[x]
 
    def Union(self, x, y):
        xset = self.find(x)
        yset = self.find(y)
        if xset == yset:
            return
 
        if self.rank[xset] < self.rank[yset]:
            self.parent[xset] = yset
 
        elif self.rank[xset] > self.rank[yset]:
            self.parent[yset] = xset
        else:
            self.parent[yset] = xset
            self.rank[xset] = self.rank[xset] + 1