import math
import numpy as np
from random import random

# save activations and derivatives#保存激活和衍生物
# implement back propagation 实现反向传递
# implement gradient descent 实现梯度下降
# implement train 实现训练
# train our net with some dummy dataset 用一些虚拟数据训练网络
# make some predictions 做出预测


class MLP:

    def __init__(self, num_inputs = 3 , num_hidden = [2,5] , num_outputs = 2 ):   # 不默认赋值，给输入
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
        
        activations = []
        for i in range(len(layers)):
            a = np.zeros(layers[i])
            activations.append(a)
        self.activations = activations

        derivatives = []
        for i in range(len(layers)-1):
            d = np.zeros((layers[i],layers[i+1]))
            derivatives.append(d)
        self.derivatives = derivatives

            





    def forward_propagate(self,inputs): # 前向传递
        activations = inputs #对于第一层（输入层）来说，激活就等于inputs
        self.activations[0] = inputs  # 储存第一层激活

        #for w in self.weights:
        for i,w in enumerate(self.weights): # enumerate 枚举，输出下标和值
            # 计算净输入
            net_inputs = np.dot(activations,w)

            # 计算激活函数
            activations = self._sigmoid(net_inputs)
            self.activations[i+1] = activations # i+1 a_3是h_2*W_2

        return activations

    def back_propagate(self,error,verbose = False): # 计算反向传播
        # error = y - a_[i+1]
        # dE/dW_i = (y - a_[i+1]) s'(h_[i+1]) a_[i]
        # s'(h_[i+1]) = s(h_[i+1])(1-h_[i+1])
        # s(h_[i+1]) = a_[i+1]

        for i in reversed(range(len(self.derivatives))):  # 反向走，所以reversed
            activations = self.activations[i+1]  # i+1? 对的导数存的比激活的少1层
            delta = error * self._sigmoid_derivative(activations) # 其实输入的是s(h(i+1))但是它又等于a(i+1)也就是activations
            current_activations = self.activations[i] # a_i
            # 需要转化为列向量，然后才进行向量的内积 
            current_activations_reshaped = current_activations.reshape(current_activations.shape[0],-1)
            delta_reshape = delta.reshape(delta.shape[0],-1).T
            self.derivatives[i] = np.dot(current_activations_reshaped, delta_reshape)

            # dE/dW_[i-1] = (y - a_[i+1]) s'(h_[i+1]) W_i s'(h_i) a[i-1]
            error = np.dot(delta,self.weights[i].T)  #更新error 复用之前的那些

            if verbose:
                print("Derivatives for W{}:\n {}".format(i,self.derivatives[i]))

        return error
    

    def gradient_descent(self, learning_rata):
        for i in range(len(self.weights)):
            weights = self.weights[i]
            #print("original W{} \n {}".format(i,weights))

            derivatives = self.derivatives[i]
            weights += derivatives * learning_rata
            #print("updating W{} \n {}".format(i,weights))


    def train(self,inputs,targets,epochs, learning_rate):
        
        for i in range(epochs):
            sum_error = 0
            for j,(input, target) in enumerate(zip(inputs,targets)):

                 # 执行前向传播
                output = self.forward_propagate(input)

                 # 计算error
                error = target - output

                # 反向传递
                self.back_propagate(error, verbose=False)

                # 梯度下降
                self.gradient_descent(learning_rate)

                sum_error += self._mse(target,output)
            # 报告error
            print("Error at epoch {}: {}".format(i ,sum_error / len(inputs)))



    def _mse(self,target, output):
        return np.average((target - output)**2 )
 
    def _sigmoid_derivative(self,x): # sigma函数的求导
        return x * (1.0 - x)   # 这个求导等于推出来的这个，1.0应该是为了浮点运算


    def _sigmoid(self,x):
         return 1.0 / (1.0 + np.exp(-x))
    




    

if __name__ == "__main__":

    # 创建一个数据集来训练神经网络，用于做加法
    inputs = np.array([[random() / 2 for _ in range(2)] for _ in range(1000)])
    # array([[0.1,0.2], [0.3,0.4]])
    targets = np.array([[i[0] + i[1]] for i in inputs])
    # array([[0.3], [0.7]])

    # 创建一个MLP
    mlp = MLP(2,[5],1)  # 默认构造初始化

    # # 创建输入
    # #inputs = np.random.rand(mlp.num_inputs)
    # inputs = np.array([0.1, 0.2])
    # targets = np.array([0.3])

    # 训练神经网络
    mlp.train(inputs , targets , 50 , 0.1) 

    # 创建虚拟数据
    input = np.array([0.3,0.1])
    targets = np.array([0.4])

    output = mlp.forward_propagate(input)
    print()
    print()
    print("Our network believes that {} + {} is equal to {}".format(input[0],input[1],output[0]))

    # # 打印结果
    # print('The network inputs is: {}'.format(inputs))
    # print("The network result is: {}".format(outputs))

    # {}是一个占位符，它表示将要插入的值的位置。.format(value)将value的值插入到占位符的位置，并返回新的字符串。
    # name = "Alice"
    # age = 25
    # message = "My name is {} and I am {} years old.".format(name, age)
    # print(message)  # 输出：My name is Alice and I am 25 years old.