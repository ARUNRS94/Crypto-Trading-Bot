import websocket, json,pprint,numpy
import datetime
import xlwings as xw

# Websocket address
Socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 60
RSI_OVERSOLD = 50
candle_closing=[]
RSI_GAIN=[]
RSI_LOSS=[]
closing_cnt = 0
RSI_GAIN_AVG=[]
RSI_LOSS_AVG=[]
RS=[]
RSI_VALUE=[]
in_position=False

# Open port definition
def on_open(ws):
    print('Connected')

# Close port definition
def on_close(ws):
    print('Disconnected')

# Xlwing - excell name and sheet name
wb = xw.Book('RSI_Value.xlsx')
sheet = wb.sheets['Sheet1']        

# Data to be updated in the excel {Cell}-Cell Number (If condition is added to avoid error for null index values)
def Excell_Write(cell):
    Date=f'A{cell}'
    close=f'B{cell}'
    change=f'C{cell}'
    gain=f'D{cell}'
    loss=f'E{cell}'
    Avg_gain=f'F{cell}'
    Avg_loss=f'G{cell}'
    rsvalue=f'H{cell}'
    rsidays=f'I{cell}'
    Status=f'J{cell}'
    BPrice=f'K{cell}'
    SPrice=f'L{cell}'
    sheet.range(Date).value = time
    sheet.range(close).value=np_closes[-1]
    if np_closes.size>=2:
        sheet.range(change).value=cur_pre_Value
    if len(RSI_GAIN)!=0:    
        sheet.range(gain).value=RSI_GAIN[-1]
    if len(RSI_LOSS)!=0:    
        sheet.range(loss).value=RSI_LOSS[-1]
    if len(RSI_GAIN_AVG)!=0:    
        sheet.range(Avg_gain).value=RSI_GAIN_AVG[-1]
    if len(RSI_LOSS_AVG)!=0:
        sheet.range(Avg_loss).value=RSI_LOSS_AVG[-1] 
    if np_closes.size>=15:
        sheet.range(rsvalue).value=RS[-1]
        sheet.range(rsidays).value=RSI_VALUE[-1]
    #if RSI_VALUE[-1] < RSI_OVERSOLD:
    #    if in_position == False:    
     #       sheet.range(SPrice).value = Sell_Price
    if in_position:    
        sheet.range(Status).value=status 
        sheet.range(BPrice).value = Buy_Price  
    else:
        sheet.range(Status).value="Relax"    
    

def on_message(ws,message):                     #Data from websocket
    jmessage=json.loads(message)
    candle=jmessage['k']                        #Candle Data 
    end_candle=candle['x']                      #Candle End Ack
    end_price=candle['c']                       #End Candle Price
    if end_candle:
        global time
        global np_closes
        global cur_pre_Value
        global in_position
        global status
        global Buy_Price
        global Sell_Price
        cell=0                                  #Intialize cell value as zero
        print (" ")
        status = ""
        time=datetime.datetime.now()            #Timestamp
        print (time)
        candle_closing.append(float(end_price)) #Appending close value to list
        np_closes = numpy.array(candle_closing) #List to numpy
        print(np_closes)
        print("closing_price {}".format(candle_closing[-1])) #printing last index from numpy
        print("closing_Size {}".format(np_closes.size))        #printing size of numpy
        if np_closes.size>=2:
            cur_pre_Value=round((np_closes[-2]-np_closes[-1]),4) #Sub last two closing values 
            print ("cur_pre {}".format(cur_pre_Value))
            if cur_pre_Value > 0:                                 #If last two values are greater than zero it is appended in RSI_LOSS
                RSI_LOSS.append(float(cur_pre_Value))
                RSI_GAIN.append(0)                                #Zero is appended to avoid duplication of data
                print("Rsi_Loss {}".format(RSI_LOSS))
                print("Rsi_Gain {}".format(RSI_GAIN))
            if cur_pre_Value < 0:                                 #If last two values are Lesser than zero it is appended in RSI_GAIN
                RSI_GAIN.append(float(cur_pre_Value*(-1)))
                RSI_LOSS.append(0)                                #Zero is appended to avoid duplication of data
                print("Rsi_Gain {}".format(RSI_GAIN)) 
                print("Rsi_Loss {}".format(RSI_LOSS))
            if cur_pre_Value == 0:                                  #If last two values are zero appending zero
                RSI_GAIN.append(0)
                RSI_LOSS.append(0)
                print("Rsi_Gain {}".format(RSI_GAIN)) 
                print("Rsi_Loss {}".format(RSI_LOSS))    
            if (np_closes.size) == 15:                                          #If the closing count reaches 15(For RSI Period 14) AVG_Gain and AVG_Loss is calculated
                    in_position = False
                    RSI_GAIN_AVG.append(round((sum(RSI_GAIN)/14),5))            #RSI_GAIN_AVG=(sum(RSI_GAIN)/14)
                    RSI_LOSS_AVG.append(round((sum(RSI_LOSS)/14),5))            #RSI_Loss_AVG=(sum(RSI_LOSS)/14)
                    RS.append(round((RSI_GAIN_AVG[-1]/RSI_LOSS_AVG[-1]),5))     #Calculating RS for last index of RSI_GAIN_AVG and RSI_Loss_AVG RS=(RSI_GAIN_AVG/RSI_LOSS_AVG)
                    print("Rsi_Gain_Avg {}".format(RSI_GAIN_AVG))
                    print("Rsi_Loss_Avg {}".format(RSI_LOSS_AVG))
                    print("Rsi_Rs {}".format(RS))
                    RSI_VALUE.append(round((100-((100)/(1+RS[-1]))),4))         #RSI CALCULATION RSI=(100-((100)/(1+RS)))
                    print("Rsi_Value{}".format(RSI_VALUE))
            elif (np_closes.size) > 15:                                         #If the closing count above 15(For RSI Period 14) AVG_Gain and AVG_Loss is calculated
                    RSI_GAIN_AVG.append(round(((((RSI_GAIN_AVG[-1])*13)+RSI_GAIN[-1])/14),5))       #RSI_GAIN_AVG=((Prev_RSI_GAIN_AVG)*13)+Curr_RSI_GAIN)/14)
                    print("Rsi_Gain_Avg {}".format(RSI_GAIN_AVG))
                    RSI_LOSS_AVG.append(round(((((RSI_LOSS_AVG[-1])*13)+RSI_LOSS[-1])/14),5))       #RSI_Loss_AVG=((Prev_RSI_Loss_AVG)*13)+Curr_RSI_Loss)/14)
                    print("Rsi_Loss_Avg {}".format(RSI_LOSS_AVG))
                    RS.append(round((RSI_GAIN_AVG[-1]/RSI_LOSS_AVG[-1]),5))
                    print("Rsi_Rs {}".format(RS))
                    RSI_VALUE.append(round((100-((100)/(1+RS[-1]))),4))
                    print("Rsi_Value{}".format(RSI_VALUE))
     
        if (np_closes.size)>= 15:
            if RSI_VALUE[-1] > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought! Sell!")
                    in_position = False
                    status = "Sold!"
                    Sell_Price=candle_closing[-1]
                else:
                    print("It is overbought, We have nothing to Sell!")
                    status = "Nothing to Sell"

            if RSI_VALUE[-1] < RSI_OVERSOLD:
                if in_position:
                    print("It is oversold, but you already own it, HOLD!")
                    status = "Hold!!!"
                else:
                    print("Oversold! Buy!")
                    in_position = True
                    status = "Bought"
                    Buy_Price = candle_closing[-1]  
     

        cell = int(np_closes.size)              #Close count is used to increment cell value in excel
        cell = cell+1            
        Excell_Write(cell)                               #Calling Excell write fn
              
                #pprint.pprint(jmessage)

def on_error(ws):
    print('Error')    
    
ws=websocket.WebSocketApp(Socket, on_open= on_open, on_close= on_close, on_message= on_message, on_error = on_error)
ws.run_forever()