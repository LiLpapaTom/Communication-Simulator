Next_arrival_time = 0
sum_of_service_times = 0
Number_of_ongoing_calls = 0

#Thomas Papaloukas
from datetime import datetime
import random
import math

class Element:
    def __init__(self,timein,timeout,occupied,position):
        self.timein = timein
        self.timeout = timeout
        self.occupied = occupied
        self.position = position
    def get_timein(self):
        return self.timein
    def get_timeout(self):
        return self.timeout
    def get_occupied(self):
        return self.occupied
    def get_position(self):
        return self.position
    def set_timein(self, timein):
        self.timein = timein
    def set_timeout(self, timeout):
        self.timeout = timeout
    def set_occupied(self, occupied):
        self.occupied = occupied
    def set_position(self, position):
        self.position = position

def Power_calc(distance):
    # λ = c speed / frequency
    l = 299792458/(847*(pow(10,6)))
    x = pow(4*(math.pi)*100/l,2)
    d0 = 10*math.log10(x)
    d = pow(distance/d0,3)
    L = d0 + 10 *math.log10(d)

    P = 18
    Pr = P * pow((l/4*math.pi*distance),2)
    #Power received
    print("Power Received: ",L/Pr," SINR: ",SINR(L/Pr,L))
    return L/Pr

def SINR(power, pathloss):
        return power/1.12*pow(10,-14)

def MCapacity(Channels):
    #list.append(Element(0,0,0,'\0'))
    list = []
    for i in range(0,int(Channels)):
        list.append(Element(0,0,0,0))
    return list

def Event():
    #Generate Double random number in range [0,RAND_MAX]
    rand = random.uniform(0,32767)
    pro = rand/32768
    #print(pro)
    return pro

def Poisson(average):
    rand = 0
    while rand == 0:
        rand = Event()
        #print(rand)
    #Compute exponential delay
    log = (math.log(rand))
    delay = float(-1)*float(average)*(log)
    return delay

def Uncheck(list, Totaltime):
    global Number_of_ongoing_calls
    for i in list:
        #print(element)
        if i.get_timeout() < Totaltime and i.get_occupied() == 1:
            temp = i.get_timeout()
            print("Call ended at ",i.get_timeout())
            print("Arrived at ",i.get_timein())
            i.set_timein(0)
            i.set_timeout(0)
            i.set_occupied(0)
            Number_of_ongoing_calls -= 1

def Check(list, Call_duration, Next_arrival_time):
    global Number_of_ongoing_calls
    flag = 0
    for i in list:
        if i.get_occupied() == 0:
            #print("cantstop")
            i.set_timein(Next_arrival_time)
            i.set_timeout(Next_arrival_time+Poisson(Call_duration))
            i.set_occupied(1)
            i.set_position(random.uniform(550,3000))
            print("Distance from BS", "%.2f" %i.get_position()," meters")
            power = Power_calc(i.get_position())
            #print("Received power: ", power," SINR: ",SINR(power))
            #print(i.get_timein(), i.get_timeout(), i.get_occupied())
            Number_of_ongoing_calls += 1
            flag = 1
            break
    return flag

def ErlangB(n ,A):
    if n == 0:
        return 1
    else:
        return ((A*ErlangB(int(n)-1,A))/int(n))/(1+(A*ErlangB(int(n)-1,A))/int(n))
        #return (A*ErlangB(n-1,A)/n)/(1+(A*ErlangB(n-1,A))/n)

def main():
    global Number_of_ongoing_calls
    Channels = input("Give number of channels at sever: ")
    #Call_total_number = input("Give number of incoming calls: ")
    Call_duration = input("Give call durations (in seconds): ")
    Interarrival = input("Give interarrival time: ")

    A = float(Call_duration)*float(Interarrival)
    Pbt = ErlangB(Channels, A)

    incoming_calls_counter = 0
    Accepted_calls_counter = 0
    Blocked_calls_counter = 0
    Totaltime = 0.0
    Next_arrival_time = 0.0
    Sum_interarrival_times = 0
    Next_arrival_time = 0
    Sum_interarrival_times = 0
    counter = 0
    steps = 0
    Pb = 0
    #List containing calls
    list = MCapacity(Channels)

    #Generate a random 1x10 distribution for occurence 2: (change if need)
    Next_arrival_time += float(Poisson(float(Interarrival)))
    flag = True
    while flag:
    #while incoming_calls_counter < int(Call_total_number):
        previous_Totaltime = Totaltime
        Totaltime = Next_arrival_time

        incoming_calls_counter += 1
        Uncheck(list, Totaltime)

        print("------------Incoming Call---------------")
        Accepted = Check(list, Call_duration, Next_arrival_time)
        if Accepted == 1:
            Accepted_calls_counter += 1
            print("Call Accepted at ",Totaltime)
        else:
            Blocked_calls_counter += 1
            print("Call Blocked at ",Totaltime)

        temp_Next_arrival_time = Next_arrival_time
        Next_arrival_time+=Poisson(Interarrival)
        Sum_interarrival_times+=(Next_arrival_time-temp_Next_arrival_time)


        Pb =  Blocked_calls_counter/incoming_calls_counter
        #Pbt = ErlangB(Channels, Pb)
        print("Block values: Pbt:",Pbt," Pb:" ,Pb)
        print("----------------------------------------")
        #if |pbt-pb|*100 <= 2, exit programm
        if abs((Pb-Pbt)*100) <= 2 and Blocked_calls_counter != 0:
            flag = False
            #for 15 more calls
            for i in range(15):
                previous_Totaltime = Totaltime
                Totaltime = Next_arrival_time

                incoming_calls_counter += 1
                Uncheck(list, Totaltime)

                print("------------Incoming Call---------------")
                Accepted = Check(list, Call_duration, Next_arrival_time)
                if Accepted == 1:
                    Accepted_calls_counter += 1
                    print("Call Accepted at ",Totaltime)
                else:
                    Blocked_calls_counter += 1
                    print("Call Blocked at ",Totaltime)

                temp_Next_arrival_time = Next_arrival_time
                Next_arrival_time+=Poisson(Interarrival)
                Sum_interarrival_times+=(Next_arrival_time-temp_Next_arrival_time)


                Pb =  Blocked_calls_counter/incoming_calls_counter
                #Pbt = ErlangB(Channels, Pb)
                print("Block values: Pbt:",Pbt," Pb:" ,Pb)
                print("----------------------------------------")


    print("Erlang target = ", Pbt*100)
    print("\n \n Mean Interarrival=", Sum_interarrival_times/incoming_calls_counter)
    print("\n \n Total number of incoming calls=", incoming_calls_counter)
    print("\n \n Accepted calls =", Accepted_calls_counter)
    print(" Percentage of accepted calls=", float(100*Accepted_calls_counter)/incoming_calls_counter,"%")
    print("\n \n Blocked calls=", Blocked_calls_counter)
    print(" Percentage of blocked calls=", float(100*Blocked_calls_counter)/incoming_calls_counter, "% \n")

main()
