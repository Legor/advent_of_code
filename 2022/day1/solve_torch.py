from utils import input, test_results
from torch.utils.data import Dataset, DataLoader
from torch.nn.functional import pad
import torch


class TextInputData(Dataset):
    def __init__(self, filename):
        self._data = [list(map(int, sp.split())) for sp in input(split_on='\n\n')]
        # use max sequence length to pad all to the same size
        max_l = max([len(x) for x in self._data])
        # build tensor with padded data
        self._data = torch.stack([pad(torch.tensor(x), [0, max_l - len(x)]) for x in self._data])
        # sum individual sequences and sort
        self._data, _ = torch.sort(torch.sum(self._data, 1), descending=True)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, idx):
        return self._data[idx]


def solve(top_n=1):
    """Solve first or second part of the puzzle"""
    # use batch size to get the top n entries
    dl = DataLoader(TextInputData('input.txt'), batch_size=top_n, shuffle=False)
    #  return sum of top n entries
    return torch.sum(next(iter(dl)))


if __name__ == "__main__":
    test_results(solve(), solve(3))
