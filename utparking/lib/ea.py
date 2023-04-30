import numpy as np
import multiprocessing

class EA:
    def __init__(self, runner, seed=3141):
        self.exp = runner
        self.seeder = np.random.SeedSequence(seed)
        np.random.seed(seed)
        self.num_students = self.exp.num_students()

    def uniform_crossover(self, p_c, p1, p2):
        """
        :param p_c: probability of crossover
        :param p1: parent 1
        :param p2: parent 2
        """
        if (np.random.random() < p_c):
            ind_len, = p1.shape
            c1 = np.zeros_like(p1)
            c2 = np.zeros_like(p2)
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

    def trn_selection(self, fitnesses, ts):
        raise NotImplementedError("use global trn_selection")
        tourn = np.random.choice(range(len(fitnesses)), ts, replace=False)
        fit = [fitnesses[i] for i in tourn]
        best = np.argmax(fit)
        ret = tourn[best]

        return ret
    
    def run(self, generations=100, p_c=0.5, p_m=0.01):
        # self.exp.setup_run(student_genomes=children)
        ind_len = 18

        population = np.random.randint(0,2,(self.num_students, ind_len), dtype=np.uint8)
        mean_fits = []
        max_fits = []

        for g in range(generations):
            children = np.zeros((self.num_students, ind_len), dtype=np.uint8)
            self.exp.setup_run(student_genomes=population)
            fitnesses = self.exp.run()
            mean_fits.append(np.mean(fitnesses))
            max_fits.append(np.max(fitnesses))

            print("Generation: %d, Mean Fitness: %f, Max Fitness: %f" % (g, mean_fits[-1], max_fits[-1]))

            print("start tourn selec")
            fs = [fitnesses]*self.num_students
            tss = [3]*self.num_students
            seeds = self.seeder.spawn(self.num_students)
            with multiprocessing.Pool(12) as pool:
                parents = pool.map(trn_selection, zip(fs, tss, seeds))
            print('done')

            print("start crossover/mutation")
            for i in range(0, (self.num_students//2)*2, 2):
                c1, c2 = self.uniform_crossover(p_c, population[parents[i]], population[parents[i+1]])
                c1 = self.mutation(p_m, c1)
                c2 = self.mutation(p_m, c2)
                children[i,:] = c1[:]
                children[i+1,:] = c2[:]
            print('done')

        population = children

        return mean_fits, max_fits

def trn_selection(args):
    fitnesses, ts, gen = args
    gen = np.random.default_rng(gen)
    tourn = gen.choice(range(len(fitnesses)), ts, replace=False)
    fit = [fitnesses[i] for i in tourn]
    best = np.argmax(fit)

    return tourn[best]
