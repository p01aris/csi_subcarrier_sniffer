# -*- coding: utf-8 -*-
import time;
import threading;
import string;
import array;
import random;
#import numpy;

class thread_manager(threading.Thread): #The timer class is derived from the class threading.Thread
    #attribut
    def __init__(self,node,interval,lte_node_num,wifi_node_num):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.node= node;
        self.rf_client1=None;
        self.transmit_interval=interval;
        self.lte_node_num=lte_node_num;
        self.wifi_node_num=wifi_node_num;

        self.use_freq=[0,1,2,3,4,5,6,7,8,9];
        self.subcarrier_append=[];

        for i in range(0,10-lte_node_num):
            self.subcarrier_append.append(i+10);

        if 'WIFI' in node:
            self.rf_client1=WIFI_client(node,interval,self.use_freq,self.subcarrier_append);
        elif 'LTE' in node:
            self.rf_client1=LTE_client(node,interval,self.use_freq);
        if 'LAA' in node:
            self.rf_client1=LAA_client(node,interval,self.use_freq);
        elif 'LASI' in node:
            self.rf_client1=LASI_client(node,interval,self.use_freq);
    def run(self): #Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:
            #run in thread
            self.rf_client1.transmit();
    def stop(self):
        self.thread_stop = True
        print(self.rf_client1.node_name+' transmit:'+str(self.rf_client1.data_num));
        print(self.rf_client1.node_name+' conflic:'+str(self.rf_client1.confict_num));

class air_ferq():
    def __init__(self):
        self.freq=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    def check_freq(self,use_freq:array):
        for fq in use_freq:
            if self.freq[fq]!=0:
                #print('air is busy\n');
                return False;
        return True;
    def transmit(self,use_freq,nodes):
        for fq in use_freq:
            self.freq[fq]=nodes;
        #print(self.freq);

    def leave(self,use_freq):
        for fq in use_freq:
            self.freq[fq]=0;
        #print(self.freq);

class LTE_client():
    def __init__(self,node_name,interval,use_freq):
        self.transmit_interval= interval;
        self.transmit_time=0.5; #common 0.5ms
        self.confict_num=0;
        self.use_freq=use_freq;
        self.node_name=node_name;
        self.data_num=0;
    def transmit(self):
        #传输前不监听
            air_space.transmit(self.use_freq,self.node_name);
            time.sleep(self.transmit_time);
            air_space.leave(self.use_freq);
            self.data_num=self.data_num+len(self.use_freq);
            #print(self.node_name+' transrate'+ str(self.data_num));
            time.sleep(self.transmit_interval);
            # print(self.node_name+' conflic'+str(self.confict_num));
            # time.sleep(self.transmit_interval);

class WIFI_client():
    def __init__(self,node_name,interval,use_freq,use_append_freq):
        self.transmit_interval= interval;
        self.transmit_time=0.5; #min28ns, max
        self.confict_num=0;
        self.use_freq=use_freq;
        self.use_append_freq=use_append_freq;
        self.node_name=node_name;
        self.data_num=0;
    def transmit(self):
        #传输前监听
        if air_space.check_freq(self.use_freq):
            air_space.transmit(self.use_freq,self.node_name);
            time.sleep(self.transmit_time);
            air_space.leave(self.use_freq);
            self.data_num=self.data_num+len(self.use_freq);
            #print(self.node_name+' transrate'+ str(self.data_num));
            time.sleep(self.transmit_interval);
        elif air_space.check_freq(self.use_append_freq):
            air_space.transmit(self.use_append_freq,self.node_name);
            time.sleep(self.transmit_time);
            air_space.leave(self.use_append_freq);
            self.data_num=self.data_num+len(self.use_append_freq);
            #print(self.node_name+' transrate'+ str(self.data_num));
            time.sleep(self.transmit_interval);
        else:
            self.confict_num+=1;
            #print(self.node_name+' conflic'+str(self.confict_num));
            time.sleep(self.transmit_interval);

class LAA_client():
    def __init__(self,node_name,interval,use_freq):
        self.transmit_interval= interval;
        self.transmit_time=0.5;
        self.confict_num=0;
        self.use_freq=use_freq;
        self.node_name=node_name;
        self.data_num=0;
    def transmit(self):
        #传输前监听
        if air_space.check_freq(self.use_freq):
            air_space.transmit(self.use_freq,self.node_name);
            time.sleep(self.transmit_time);
            air_space.leave(self.use_freq);
            self.data_num=self.data_num+len(self.use_freq);
            #print(self.node_name+' transrate'+ str(self.data_num));
            time.sleep(self.transmit_interval+0.1*random.random());
        else:
            self.confict_num+=1;
            #print(self.node_name+' conflic'+str(self.confict_num));
            time.sleep(self.transmit_interval);
class LASI_client():
    def __init__(self,node_name,interval,use_freq):
        self.transmit_interval= interval;
        self.transmit_time=0.5;
        self.confict_num=0;
        self.use_freq=use_freq;
        self.node_name=node_name;
        self.data_num=0;
    def transmit(self):
        #传输前监听
        #if air_space.check_freq(self.use_freq):
            air_space.transmit(self.use_freq,self.node_name);
            time.sleep(self.transmit_time);
            air_space.leave(self.use_freq);
            self.data_num=self.data_num+len(self.use_freq);
            #print(self.node_name+' transrate'+ str(self.data_num));
            time.sleep(self.transmit_interval);
        #else:
            # self.confict_num+=1;
            # #print(self.node_name+' conflic'+str(self.confict_num));
            # time.sleep(self.transmit_interval);

def start_run(node_array:array,execute_time,interval,lte_node_num,wifi_node_num):
    #Creat threads array for get stock info
    thread_array=[];
    print('start thread init\n');
    #Add thread to array
    for nums in node_array:
         thread_temp=thread_manager(nums,interval,lte_node_num,wifi_node_num);
         thread_array.append(thread_temp);
    #start every thread
    for thread_temp in thread_array:
        thread_temp.start();
    time.sleep(execute_time);

    #stop every thread

    for thread_temp in thread_array:
        thread_temp.stop();

if __name__ == '__main__':

    print('LTE:Change');
    ap_num=[];
    for i in range(1,10):
        print('New Game');
        ap_num=[];
        ap_num.append('WIFI1');
        for j in range(0,i):
            ap_num.append('LASI'+str(j));
        air_space =air_ferq();
        print(ap_num);
        start_run(ap_num,10,0.1,i,1);#parameter:ap_name,exe_time,interval_time,lte_node_num,wifi_node_num
    print('WIFI:Change');
    for i in range(1,10):
        ap_num=[];
        ap_num.append('LASI1');
        for j in range(1,i):
            ap_num.append('WIFI'+str(j));
        air_space =air_ferq();
        start_run(ap_num,10,0.1,1,i);#parameter:ap_name,exe_time,interval_time,te_node_num,wifi_node_num
    # ap_num=[];
    # ap_num.append('WIFI1'); #股票代码
    # # ap_num.append('WIFI2');
    # # ap_num.append('WIFI3');
    # # ap_num.append('WIFI4');
    # # ap_num.append('WIFI5');
    # # ap_num.append('WIFI6');
    # # ap_num.append('WIFI7');
    # # ap_num.append('WIFI8');
    # # ap_num.append('WIFI9');
    # # ap_num.append('WIFI10');
    # #ap_num.append('LTE1');
    # #ap_num.append('LAA1');    
    print('DUTY_CYCLE:Change');
    ap_num=[];
    ap_num.append('LASI1');
    ap_num.append('WIFI1');
    ap_num.append('WIFI2');
    ap_num.append('WIFI3');
    ap_num.append('WIFI4');
    i=0;
    while i < 0.5:
        print('intercal:'+str(i));
        start_run(ap_num,10,i,4,4);
        i=i+0.1;
    # ap_num.append('LASI1');
    # #ap_num.append('WIFI5');
    # #ap_num.append('WIFI2');
    # #ap_num.append('WIFI2');
    # air_space = air_ferq();
    # start_run(ap_num,10); #第二个参数是执行时间，1就是执行1秒
