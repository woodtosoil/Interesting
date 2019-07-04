import torch as t
from IPython import display
%matplotlib inline
from matplotlib import pyplot as plt

t.manual_seed(1000)

def get_fake_data(batch_size=8):
    x=t.rand(batch_size,1)*20
    y=x*2+(1+t.rand(batch_size,1))*3
    return x,y
x,y=get_fake_data()
plt.scatter(x.squeeze().numpy(),y.squeeze().numpy())