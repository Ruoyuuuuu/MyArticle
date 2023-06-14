import math
import numpy as np

class MLP:

    def __init__(self, num_inputs = 3, num_hidden = [3, 5], num_outputs = 2):  
        # num_inputs：表示输入层的神经元数量，默认为3。
        # num_hidden：表示隐藏层的神经元数量，以列表形式表示，默认为[2, 5]，表示有两个隐藏层，第一个隐藏层有2个神经元，第二个隐藏层有5个神经元。
        # num_outputs：表示输出层的神经元数量，默认为2。
        self.num_inputs = num_inputs   # 赋值给实例本身
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

        # 统合建立一个层数的向量，代表每一层拥有几个神经元
        layers = [self.num_inputs] + self.num_hidden + [self.num_outputs] # [3，3，5，2]; []强制转换为数组

        #初始化随机权重
        self.weights = []
        for i in range(len(layers)-1):  # 权重只需要比层数少1就行
            w = np.random.rand(layers[i],layers[i+1]) # 建立一个随机i*j的权重矩阵，i行为本层神经元个数，j列为下一层神经元个数
            # rand（）函数，0～1之间随机数
            self.weights.append(w) #加入一个w

    def forward_propagate(self,inputs): # 前向传递
        activations = inputs #对于第一层（输入层）来说，激活就等于inputs

        for w in self.weights:
            # 计算净输入
            net_inputs = np.dot(activations,w)

            # 计算激活函数
            activations = self._sigmoid(net_inputs)

        return activations

    def _sigmoid(slef,x):
         return 1 / (1 + np.exp(-x))
    

if __name__ == "__main__":
    # 创建一个MLP
    mlp = MLP()  # 默认构造初始化

    # 创建输入
    inputs = np.random.rand(mlp.num_inputs)

    # 执行前向传播
    outputs = mlp.forward_propagate(inputs)

    # 打印结果
    print('The network inputs is: {}'.format(inputs))
    print("The network result is: {}".format(outputs))

    # {}是一个占位符，它表示将要插入的值的位置。.format(value)将value的值插入到占位符的位置，并返回新的字符串。
    # name = "Alice"
    # age = 25
    # message = "My name is {} and I am {} years old.".format(name, age)
    # print(message)  # 输出：My name is Alice and I am 25 years old.