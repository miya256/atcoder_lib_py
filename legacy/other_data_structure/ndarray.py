#indexの計算が遅いっぽい
class NdArray:
    def __init__(self, shape, init=0):
        self.shape = shape
        self.stride = list(shape)
        for i in range(len(shape)-1, 0, -1):
            self.stride[i-1] *= self.stride[i]
        self.size = self.stride[0]
        self.data = [init] * self.size
    
    def _index(self, indices):
        idx = 0
        for i, s in zip(indices, self.shape):
            idx *= s
            idx += i
        return idx
    
    def __getitem__(self, indices):
        return self.data[self._index(indices)]
    
    def __setitem__(self, indices, value):
        self.data[self._index(indices)] = value
    
    @property
    def dim(self):
        return len(self.shape)
    
    def _print_str(self, data, dim):
        if dim == 1:
            return str(data)
        string = ["["]
        for i in range(self.shape[-dim]):
            string.append(self._print_str(data[i*self.stride[-dim+1]: (i+1)*self.stride[-dim+1]], dim-1))
            string.append("\n" + " "*(self.dim-dim+(i!=self.shape[-dim]-1)))
        string.append("]")
        return ''.join(string)
    
    def __repr__(self):
        return self._print_str(self.data, len(self.shape))