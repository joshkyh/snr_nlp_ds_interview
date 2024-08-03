import matplotlib.pyplot as plt
import umap
import pandas as pd
import sklearn

if __name__ == "__main__":
    test_dfr = pd.DataFrame({'clientid': [1, 2, 3, 4, 5], 'age': [20, 25, 30, 35, 40]})
    assert test_dfr.shape[0] == 5
    assert test_dfr.shape[1] == 2

    um_list = dir(umap)
    assert len(um_list) > 1

    sklearn_list = dir(sklearn)
    assert len(um_list) > 1

    plt_list = dir(plt)
    assert len(plt_list) > 1
 
    print("Test passed")