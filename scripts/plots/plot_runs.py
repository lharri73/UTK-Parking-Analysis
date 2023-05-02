import pickle
import numpy as np

def load_data():
    with open('results/multirun_largest.pkl', 'rb') as f:
        data = pickle.load(f)
    print(len(data))
    for run in data:
        num_checked, time_spent = run
        for stu in range(len(num_checked)):
            yield num_checked[stu], time_spent[stu]
        
    # for d_f in data:

        # for d in d_f:
        #     print(len(d))
        #     yield d[0], d[1]

def main():
    data = np.array(list(load_data()))
    print(data.shape)

    print(np.mean(data, axis=0))
    

if __name__ == "__main__":
    main()
