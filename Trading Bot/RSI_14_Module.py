import numpy,datetime

candle_price=[]
candle_closing=0.0
RSI_GAIN=[]
RSI_LOSS=[]
RSI_GAIN_AVG=[]
RSI_LOSS_AVG=[]
RS=[]
RSI_VALUE=[]
n=10

def RSI_cal(candle_closing): 
    ''' Give end candle price as input '''
    global np_closes
    global cur_pre_Value
    cur_pre_Value = 0
    time=datetime.datetime.now()            #Timestamp
    candle_price.append(float(candle_closing))
    np_closes = numpy.array(candle_price) #candle_closing_Value to numpy
    if np_closes.size>=2:
        cur_pre_Value=round((np_closes[-1]-np_closes[-2]),4) #Sub last two closing values 
        if cur_pre_Value < 0:                                 #If last two values are greater than zero it is appended in RSI_LOSS
            RSI_LOSS.append(float(cur_pre_Value*(-1)))
            RSI_GAIN.append(0)                                #Zero is appended to avoid duplication of data
            
        if cur_pre_Value > 0:                                 #If last two values are Lesser than zero it is appended in RSI_GAIN
            RSI_GAIN.append(float(cur_pre_Value))
            RSI_LOSS.append(0)                                #Zero is appended to avoid duplication of data
            
        if cur_pre_Value == 0:                                  #If last two values are zero appending zero
            RSI_GAIN.append(0)
            RSI_LOSS.append(0)
        if (np_closes.size) == 15:                                          #If the closing count reaches 15(For RSI Period 14) AVG_Gain and AVG_Loss is calculated
            RSI_GAIN_AVG.append(round((sum(RSI_GAIN)/14),5))            #RSI_GAIN_AVG=(sum(RSI_GAIN)/14)
            RSI_LOSS_AVG.append(round((sum(RSI_LOSS)/14),5))            #RSI_Loss_AVG=(sum(RSI_LOSS)/14)
            RS.append(round((RSI_GAIN_AVG[-1]/RSI_LOSS_AVG[-1]),5))     #Calculating RS for last index of RSI_GAIN_AVG and RSI_Loss_AVG RS=(RSI_GAIN_AVG/RSI_LOSS_AVG)
            RSI_VALUE.append(round((100-((100)/(1+RS[-1]))),4))         #RSI CALCULATION RSI=(100-((100)/(1+RS)))
        elif (np_closes.size) > 15:                                         #If the closing count above 15(For RSI Period 14) AVG_Gain and AVG_Loss is calculated
            RSI_GAIN_AVG.append(round(((((RSI_GAIN_AVG[-1])*13)+RSI_GAIN[-1])/14),5))       #RSI_GAIN_AVG=((Prev_RSI_GAIN_AVG)*13)+Curr_RSI_GAIN)/14)
            RSI_LOSS_AVG.append(round(((((RSI_LOSS_AVG[-1])*13)+RSI_LOSS[-1])/14),5))       #RSI_Loss_AVG=((Prev_RSI_Loss_AVG)*13)+Curr_RSI_Loss)/14)
            RS.append(round((RSI_GAIN_AVG[-1]/RSI_LOSS_AVG[-1]),5))
            RSI_VALUE.append(round((100-((100)/(1+RS[-1]))),4))
        if (np_closes.size) > 30:
            del RSI_VALUE[:n] 
            del RS[:n]
            del RSI_LOSS[:n]
            del RSI_LOSS_AVG[:n]
            del RSI_GAIN[:n]
            del RSI_GAIN_AVG[:n]   
            del candle_price[:n]