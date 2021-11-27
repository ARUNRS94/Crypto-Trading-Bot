import websocket, json,pprint,numpy
import datetime

import RSI_14_Module as RM

# Websocket address
Socket = "wss://stream.binance.com:9443/ws/bnbusdt@kline_1m"

RSI_OVERBOUGHT = 60
RSI_OVERSOLD = 50
in_position = False
Buy_Price=[]
Sell_Price=[]

# Open port definition
def on_open(ws):
    print('Connected')

# Close port definition
def on_close(ws):
    print('Disconnected')

def on_message(ws,message):                     #Data from websocket
    global in_position
    jmessage=json.loads(message)
    candle=jmessage['k']                        #Candle Data 
    end_candle=candle['x']                      #Candle End Ack
    end_price=candle['c']                       #End Candle Price
    if end_candle:
        RM.RSI_cal(end_price)
        print(RM.np_closes.size)
        print('RSI Value')
        print(RM.RSI_VALUE)
        if len(RM.RSI_VALUE)>0:
            if RM.RSI_VALUE[-1] > RSI_OVERBOUGHT:
                    if in_position:
                        print("Overbought! Sell! Sell! Sell!")
                        in_position = False
                        Sell_Price.append(float(end_price))
                    else:
                        print("It is overbought, but we don't own any. Nothing to do.")
            if RM.RSI_VALUE[-1] < RSI_OVERSOLD:
                    if in_position:
                        print("It is oversold, but you already own it, nothing to do.")
                    else:
                        print("Oversold! Buy! Buy! Buy!")
                        in_position = True
                        Buy_Price.append(float(end_price))
        print('Buy Price')
        print(Buy_Price)
        print('Sell Price')
        print(Sell_Price)

def on_error(ws):
    print('Error')    
    
ws=websocket.WebSocketApp(Socket, on_open= on_open, on_close= on_close, on_message= on_message, on_error = on_error)
ws.run_forever()