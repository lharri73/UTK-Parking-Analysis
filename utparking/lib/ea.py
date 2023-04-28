import numpy as np

class EA:
    def __init__(self, runner):
        self.exp = runner

    def uniform_crossover(self, p_c, p1, p2):
        """
        :param p_c: probability of crossover
        :param p1: parent 1
        :param p2: parent 2
        """
        if (np.random.random() < p_c):
            ind_len, = p1.shape
            c1 = np.zeros(ind_len)
            c2 = np.zeros(ind_len)
            rand = np.random.random((ind_len,))
            swap_msk = rand < 0.5

            c1[swap_msk] = p1[swap_msk]
            c2[swap_msk] = p2[swap_msk]
            c1[np.logical_not(swap_msk)] = p2[np.logical_not(swap_msk)]
            c2[np.logical_not(swap_msk)] = p1[np.logical_not(swap_msk)]
        else:
            c1 = p1.copy()
            c2 = p2.copy()
        return c1, c2
    
    def mutation(self, p_m, p):
        """
        :param p_m: probability of mutation
        :param p: parent genome
        """
        ind_len, = p.shape
        c = p.copy()
        rand = np.random.random((ind_len,))
        msk = rand < p_m
        c[msk] = np.logical_not(c[msk])

        return c
    
    def trn_selection(fitnesses, ts):
        tourn = np.random.choice(range(len(fitnesses)), ts, replace=False)
        tourn_fit = [fitnesses[i] for i in tourn]

        return tourn[np.argmax(tourn_fit)]

    def run(self):
        num_children = self.exp.num_students()
        children = np.zeros((num_children, 16))
        self.exp.setup_run(student_genomes=children)
        
