from utils.metrics import mae


def evaluate():

    pred = [10,12,15]
    true = [11,14,15]

    print("MAE:", mae(pred,true))


if __name__ == "__main__":

    evaluate()