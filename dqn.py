import flappybird as fb
import tensorflow as tf
import game_functions as gf
import time
import random
import numpy as np
from collections import deque
N_exp_replay=50000
number_actions=2
actions=['up','down']
gamma=0.99
total_episodes=10000
init_epsilon=1
C_target_update=1000
batch=32
N_start_train=10000
# weight-bias initialize defination
def weight_varibale(shape):
    initial=tf.truncated_normal(shape,stddev=0.01)
    return tf.Variable(initial)
def bias_variable(shape):
    initial=tf.constant(0.01,shape=shape)
    return tf.Variable(initial)
def simpleconv2d(x,w,stride):
    return tf.nn.conv2d(x,w,strides=[1,stride,stride,1],padding="SAME")
# net aritechture create
def createnetwork():
    w_conv1,b_conv1=weight_varibale([8,8,4,32]),bias_variable([32])
    w_conv2, b_conv2 = weight_varibale([4,4,32,64]), bias_variable([64])
    w_conv3, b_conv3 = weight_varibale([3,3,64,64]), bias_variable([64])
    w_fc1,b_fc1=weight_varibale([7744,512]),bias_variable([512])
    w_fc2,b_fc2=weight_varibale([512,number_actions]),bias_variable([number_actions])
    input=tf.placeholder("float",[None,84,84,4])
    h_conv1=tf.nn.relu(simpleconv2d(input,w_conv1,4)+b_conv1)
    h_conv2=tf.nn.relu(simpleconv2d(h_conv1,w_conv2,2)+b_conv2)
    h_conv3=tf.nn.relu(simpleconv2d(h_conv2,w_conv3,1)+b_conv3)
    h_conv3_flat=tf.reshape(h_conv3,[-1,7744])
    h_fc1=tf.nn.relu(tf.matmul(h_conv3_flat,w_fc1)+b_fc1)
    pro_action=tf.matmul(h_fc1,w_fc2)+b_fc2

    return input,pro_action
# net train
def trainnetwork(input,pro_action,sess):
    yj_form_arg=tf.placeholder("float",[None])
    aj_form_arg=tf.placeholder("float",[None,number_actions])
    Q_value=tf.reduce_sum(tf.multiply(pro_action,aj_form_arg),reduction_indices=1)
    loss=tf.reduce_mean(tf.square(yj_form_arg-Q_value))
    train_step=tf.train.AdamOptimizer(1e-3).minimize(loss)
    sess.run(tf.global_variables_initializer())
    D=deque()
    C_index=0
    pro_j1_action=np.zeros([batch,number_actions])
    epsilon=init_epsilon
    for episode in range(total_episodes):
        bird,base,ai_settings,pipes,uppipes,stat= fb.game_initialize()
        stat.xt=gf.phi(gf.getframe())
        stat.st=np.stack([stat.xt,stat.xt,stat.xt,stat.xt],axis=2)
        while stat.game_active:
            if random.random()<epsilon: action_index=random.randrange(number_actions)
            else: action_index=np.argmax(pro_action.eval(feed_dict={input: [stat.st]}))
            stat.action_index[action_index],stat.action=1,actions[action_index]
            stat.action_reward=0
            fb.run_step(bird, base, ai_settings, pipes, uppipes, stat)
            stat.xt1=np.reshape(gf.phi(stat.xt1),(84,84,1))
            stat.st1=np.append(stat.st[:,:,1:4],stat.xt1,axis=2)
            D.append((stat.st,stat.action_index,stat.action_reward,stat.st1,stat.game_active))
            if len(D)>N_exp_replay: D.popleft()
            stat.st = stat.st1
            C_index+=1
            if len(D)>N_start_train:
                minibatch=random.sample(D,batch)
                st=[d[0] for d in minibatch]
                aj=[d[1] for d in minibatch]
                rj=[d[2] for d in minibatch]
                st1=[d[3] for d in minibatch]
                if C_index >= C_target_update:
                    pro_j1_action = pro_action.eval(feed_dict={input:st1})
                    C_index = 0
                yj=[]
                for i in range(0,len(minibatch)):
                    terminal=minibatch[i][4]
                    if not terminal: yj.append(rj[i])
                    else: yj.append(rj[i]+gamma*np.max(pro_j1_action[i]))
                train_step.run(feed_dict={
                    input:st,
                    aj_form_arg:aj,
                    yj_form_arg:yj})
def main():
    sess=tf.InteractiveSession()
    input,pro_action=createnetwork()
    trainnetwork(input,pro_action,sess)
main()