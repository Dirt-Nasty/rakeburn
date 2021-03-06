# Mini Flask example app.
from flask import Flask, render_template, Response, request, redirect, url_for
import time
import requests
import json
import pandas as pd
import os
from bscscan import BscScan
from datetime import datetime, timedelta
from dotenv import load_dotenv

app = Flask(__name__, static_url_path='/static')


print(
 '''
     (                    )                        (         )                                                                                              
     )\ )     (        ( /(           (            )\ )   ( /(          )                         )                                                         
    (()/(     )\       )\())  (     ( )\      (   (()/(   )\())      ( /(     (    (           ( /(     (       )                                      )    
     /(_)) ((((_)(   |((_)\   )\    )((_)     )\   /(_)) ((_)\       )\())   ))\   )(     (    )\())   ))\   ( /(   `  )    `  )         (     (      (     
    (_))    )\ _ )\  |_ ((_) ((_)  ((_)_   _ ((_) (_))    _((_)     ((_)\   /((_) (()\    )\  ((_)\   /((_)  )(_))  /(/(    /(/(         )\    )\     )\  ' 
    | _ \   (_)_\(_) | |/ /  | __|  | _ ) | | | | | _ \  | \| |     | |(_) (_))    ((_)  ((_) | |(_) (_))(  ((_)_  ((_)_\  ((_)_\       ((_)  ((_)  _((_))  
    |   /    / _ \     ' <   | _|   | _ \ | |_| | |   /  | .` |  _  | ' \  / -_)  | '_| / _ \ | / /  | || | / _` | | '_ \) | '_ \)  _  / _|  / _ \ | '  \() 
    |_|_\   /_/ \_\   _|\_\  |___|  |___/  \___/  |_|_\  |_|\_| (_) |_||_| \___|  |_|   \___/ |_\_\   \_,_| \__,_| | .__/  | .__/  (_) \__|  \___/ |_|_|_|  
                                                                                                                   |_|     |_|                              
                                                                                                                                            
                                                                                                                                            
                                                                        .%&*                                                                
                                                                         ##(&                                                               
                                                                          ##(%                                                              
                                                                           (%(%                                                             
                                     ,&, ##                                 (#(#                                                            
                                   #*      ,@#                               (%(#                                                           
                                 #* *, *&*                                    /%(#                                                          
                            ./*.%   /%.%%.  /%                                 *%(#                                                         
                            % .   ,@&   .. .*#@@/         ,%@@@@@@@@@@@@@       ,%((                                                        
                            # *.    * ,&(/%         .#@@@@@@@@@@@@@@@@@@&        ,%((.                                                      
                            ,* *,**,#..%   &     %@@@@@@@@@@@@@@@%.,(##@#         .%((.                                                     
                             % ,*.  ,, /%*//&.%@@@@@@@@@@@@@@%.         .&.         %((.                                                    
                             ,*   *. %,  .&*@@@@@@@@@@@@@@%            .@ %          %((,                                                   
                              /.    .(&#  #@@@@@@@@@@@@@*             /@. #           %((, #(*,,.,..,                                       
                           @@@@@&%(*,.   ,@@@@@@@@@@@@/   .&*     . .@@@@.#            &((/*       &                                        
                          #@#((((((#%@@@ *@@@@@@@@@@@(.      @@@@@&/#@@@@,%          ...&(/.#/,. .#                                         
                         .@@@##%&@@@@@,   @@@@@@@@@&((*      @@@@@@, @@@@,*        %.    &(/*                                               
                         &@@@@@@@@@@(     (@@@@@@@@((((      #@@@@@./ (/*%        %  **.  &(/**  *%%.                                       
                        .@@@@@@@@@@        %@@@@@@@@(((((.    .(/.,,@*  ,#&&(.    %*//,* ,.&(/(     #(                                      
                        /@@@@@@@@@*         *@@@ .@@@&((((#*   *#. &*  *&(        #  ,.  & (@(/(/&#                                         
                        %@@@@@@@@@@@@@%.      #@@   &@@@##((###,         %/       %    . &   %(/(                                           
                        &@@@@@@@@@@@@@@@@@@@&/  .@    @@@@#(((.          ,  (& ,( .(,.,  **&&#%(/#                                          
                            (&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@            *@&   .@@@ &   ,   #. %(/#                                         
                                         .*/(#%&&@@@@@@@@@@&            *.(@/   @@#@@*%%   *,   %(/#                                        
                                            ,&@@@@@@@@@&, #             ,  (#   @@@(#@@/         %#/%                                       
                                       *&@@@@@@@@@@#    ./               /.    .@@@@(((@@*        ((/%                                      
                                  /@@@@@@@@@@@@%       *,                @&.   *@@@@@@&@@@&        (#/%                                     
                             ,&@@@@@@@@@@@@&.         #                 /@@@@@*%@@@@@@@@@           /#/%                                    
                          .@@@@@@@@@@@@@/            %,                 % *@@@@@@@@@@@&              *#/&                                   
                            *@@@@@@@&.                  &(             *,    @@@@@@@(                 *#/&                                  
                              %@@@@@&                      ,&/         &       #@@,                    ,#/&                                 
                                @@@@@@@(                        /&(.  ,.                                .#/%                                
                                 /@@@@@@@@*                           *                                  /#&&                               
                                   @@@@@@@@@@.                                                            ,%%&                              
                                    ,@@@@@@@@@@%                                                            %&&                             
                                      &@@@@@@@@@@@/                                                         .%&&/                           
                                       *@@@@@@@@@@&                                                   ,&&&. .##&&&&*                        
                                       .@@@@@@@@@                                       #%#%#%&%#(%%.&%/%%#&&#(#&&&&@%.                     
                     *@@@@&*         .@@@@@@@@@/                                    %&%&&& *#&#((%/&/%&%*&&&%(&&&&%%&%%&#*.                 
                    %@@@@@@@@&     *@@@@@@@@@@ *@@@(      .                       ,&#%(##&&&&%&&&&&%# ./#&&%%&&#%##%%&&&&&&%(               
            @@@@@@* %@@@(,%@@@  .&@@@@@@@@@@( (@@@@@@,  @@@@@           *%#*  .,.%%&&%*%&%*/#/&/&&%&&&%/%&&&&&&&#((%@@%###%&%&&#            
           *@@@@@@@* @@@. #@. &@@@@@@@@@@@@,  @* &@@@& @,#@@@.          /&&#(&###&%,(%&&&*#(*%&&&&&&&&*/&&%%#%&&&%%%&###&%&&#/&&*,#         
   #@@@@@&  %@@@/    .@@@@&@@@@@@@@@@@@@@@,     %@@@@. /@@@@(.%@@@@@         /&&#&&&#(&&#,&&&&/&&&(&&/%&&%%(%&&&%%%&%&#%&&&%*&%&(% &        
   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@           ,&%%*&#&&#*%&&%**,%%&&&&#**#&&&.#(&&&%&&&&&*%&&(& #         
    %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,            *&%#&&&&%&%&&#%&&%.  #&&&&&%&%%&&#%&&&(&&&&, &             
                                                                                       *&&&@&*             *&&&%%&&&&,*% .                  
                                                                                                               .*,                          
                                                                                                                                                                                                                                                     
      _______                   _     ______  ______  _     _ ______ _______ _
     (_______)                 | |   (_____ \(_____ \| |   (_|_____ (_______|_)
      _____ _____  ____ ____   | |__  _____) )_____) ) |_____ _____) )____   _ ____  _____ ____   ____ _____
     |  ___|____ |/ ___)    \  |  _ \|  __  /(_____ (|_____  |  ____/  ___) | |  _ \(____ |  _ \ / ___) ___ |
     | |   / ___ | |   | | | |_| |_) ) |  \ \ _____) )     | | |_   | |     | | | | / ___ | | | ( (___| ____|
     |_|   \_____|_|   |_|_|_(_)____/|_|   |_(______/      |_|_(_)  |_|     |_|_| |_\_____|_| |_|\____)_____)
     ''')
@app.route('/')
def index():
    load_dotenv()
    bsc = BscScan(os.getenv("SECRET-KEY"))
    dead = '0x000000000000000000000000000000000000dead'

    moonVaults = [


        { 'add': '0x24342ba15ddfc2c8e35d4583e4f208bda0c84d04',
        'name': 'wbnb',
        'contract' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'  },
        { 'add': '0xccfc4ecc31b106a82c405941d81b2b6ede26e9bc',
        'name': 'binance-usd',
        'contract' : '0xe9e7cea3dedca5984780bafc599bd69add087d56'},
        { 'add': '0x402b67c415aeed1a88a0b8d7a67a1799f1de46e4',
        'name': 'binance-bitcoin',
        'contract' :  '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c' },
        { 'add': '0x46ab0bc682f59028f827c78d65c4d3ef74f2a396',
        'name': 'binance-eth',
        'contract' :  '0x2170ed0880ac9a755fd29b2688956bd959f933f8' },
        { 'add': '0x1ea762df2abb80b8428dfa5a1d402b6c2cd82635',
        'name': 'tether',
        'contract' :  '0x55d398326f99059ff775485246999027b3197955' },
        { 'add': '0xa7de31e6468aab2d41948686768ac051e976cab0',
        'name': 'usd-coin',
        'contract' :  '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d' },
        { 'add': '0xdcefcb8a4c39df62045ccd4e97842f414b2dd123',
        'name': 'chainlink',
        'contract' : '0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd' },
        { 'add': '0xe8038b55d7c16a979e9d588725b89e78c0cbcb48',
        'name': 'polkadot',
        'contract' : '0x7083609fce4d1d8dc0c979aab8c869ea2c873402'  },    


        ]
    
    def getTransfers(token, symbol, dec):
        #resp = bsc.get_bep20_token_transfer_events_by_contract_address_paginated(contract_address=token, page=1, offset=10000, sort='desc')
        resp = bsc.get_bep20_token_transfer_events_by_address(address=token, startblock=0, endblock=999999999, sort='desc')
        table = pd.json_normalize(resp)
        table = table[table['to']==dead]
        table = table[table['tokenSymbol']==symbol]
        table["value"] = table.value.astype(float)
        #table = table.convert_value(convert_numeric=True)
        table['adjustedValue'] = table["value"] / dec
        return(table)

    def formatDollar(value):
        return '${:,.2f}'.format(value)

    def formatClean(value):
        return '{:,.2f}'.format(value)

    def geckoPrice(ticker):
        tokenPrice = requests.get('https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd'.format(ticker))
        tokenPrice = json.loads(tokenPrice.text)[ticker]['usd']
        return tokenPrice   
      
    def getPools():

        rakePrice = requests.get('https://farm.br34p.finance/bsc/get_stats')
        rakePrice = json.loads(rakePrice.text)['priceAUTO']
        br34pPrice = geckoPrice('br34p')


        token = '0x24342BA15dDfC2c8e35D4583E4F208BDA0c84D04'

        dollRemain = []
        df = pd.DataFrame()
        br34p = pd.DataFrame()
        yield '<html><head><title>RAKEBURN.herokuapp.com | See the BURN rate!</title><link rel="icon" href="/static/favicon.ico"></head><div id="main">'
        yield '(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield ')\&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;/(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)\&nbsp;)&nbsp;&nbsp;&nbsp;(&nbsp;/(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '(()/(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)\&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)\())&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;)\&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;(()/(&nbsp;&nbsp;&nbsp;)\())&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;/(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;/(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '/(_))&nbsp;((((_)(&nbsp;&nbsp;&nbsp;&nbsp;((_)\&nbsp;&nbsp;&nbsp;)\&nbsp;&nbsp;&nbsp;&nbsp;)((_)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)\&nbsp;&nbsp;&nbsp;/(_))&nbsp;((_)\&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)\())&nbsp;&nbsp;&nbsp;))\&nbsp;&nbsp;&nbsp;)(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;)\())&nbsp;&nbsp;&nbsp;))\&nbsp;&nbsp;&nbsp;(&nbsp;/(&nbsp;&nbsp;&nbsp;`&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;`&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '(_))&nbsp;&nbsp;&nbsp;&nbsp;)\&nbsp;_&nbsp;)\&nbsp;&nbsp;&nbsp;_&nbsp;((_)&nbsp;((_)&nbsp;&nbsp;((_)_&nbsp;&nbsp;&nbsp;_&nbsp;((_)&nbsp;(_))&nbsp;&nbsp;&nbsp;&nbsp;_((_)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;((_)\&nbsp;&nbsp;&nbsp;/((_)&nbsp;(()\&nbsp;&nbsp;&nbsp;&nbsp;)\&nbsp;&nbsp;((_)\&nbsp;&nbsp;&nbsp;/((_)&nbsp;&nbsp;)(_))&nbsp;&nbsp;/(/(&nbsp;&nbsp;&nbsp;&nbsp;/(/(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)\&nbsp;&nbsp;&nbsp;&nbsp;)\&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)\&nbsp;&nbsp;\'&nbsp;<br>'
        yield '|&nbsp;_&nbsp;\&nbsp;&nbsp;&nbsp;(_)_\(_)&nbsp;|&nbsp;|/&nbsp;/&nbsp;&nbsp;|&nbsp;__|&nbsp;&nbsp;|&nbsp;_&nbsp;)&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;_&nbsp;\&nbsp;&nbsp;|&nbsp;\|&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;|(_)&nbsp;(_))&nbsp;&nbsp;&nbsp;&nbsp;((_)&nbsp;&nbsp;((_)&nbsp;|&nbsp;|(_)&nbsp;(_))(&nbsp;&nbsp;((_)_&nbsp;&nbsp;((_)_\&nbsp;&nbsp;((_)_\&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;((_)&nbsp;&nbsp;((_)&nbsp;&nbsp;_((_))&nbsp;&nbsp;<br>'
        yield '|&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;_&nbsp;\&nbsp;&nbsp;&nbsp;|&nbsp;\'&nbsp;<&nbsp;&nbsp;&nbsp;|&nbsp;_|&nbsp;&nbsp;&nbsp;|&nbsp;_&nbsp;\&nbsp;|&nbsp;|_|&nbsp;|&nbsp;|&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;|&nbsp;.`&nbsp;|&nbsp;&nbsp;_&nbsp;&nbsp;|&nbsp;\'&nbsp;\&nbsp;&nbsp;/&nbsp;-_)&nbsp;&nbsp;|&nbsp;\'_|&nbsp;/&nbsp;_&nbsp;\&nbsp;|&nbsp;/&nbsp;/&nbsp;&nbsp;|&nbsp;||&nbsp;|&nbsp;/&nbsp;_`&nbsp;|&nbsp;|&nbsp;\'_&nbsp;\)&nbsp;|&nbsp;\'_&nbsp;\)&nbsp;&nbsp;_&nbsp;&nbsp;/&nbsp;_|&nbsp;&nbsp;/&nbsp;_&nbsp;\&nbsp;|&nbsp;\'&nbsp;&nbsp;\()&nbsp;<br>'
        yield '|_|_\&nbsp;&nbsp;&nbsp;/_/&nbsp;\_\&nbsp;&nbsp;|_|\_\&nbsp;&nbsp;|___|&nbsp;&nbsp;|___/&nbsp;&nbsp;\___/&nbsp;&nbsp;|_|_\&nbsp;&nbsp;|_|\_|&nbsp;(_)&nbsp;|_||_|&nbsp;\___|&nbsp;&nbsp;|_|&nbsp;&nbsp;&nbsp;\___/&nbsp;|_\_\&nbsp;&nbsp;&nbsp;\_,_|&nbsp;\__,_|&nbsp;|&nbsp;.__/&nbsp;&nbsp;|&nbsp;.__/&nbsp;&nbsp;(_)&nbsp;\__|&nbsp;&nbsp;\___/&nbsp;|_|_|_|&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|_|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|_|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.%&*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;##(&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;##(%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(%(%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&,&nbsp;##&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(#(#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,@#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(%(#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#*&nbsp;*,&nbsp;*&*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/%(#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;./*.%&nbsp;&nbsp;&nbsp;/%.%%.&nbsp;&nbsp;/%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*%(#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%&nbsp;.&nbsp;&nbsp;&nbsp;,@&&nbsp;&nbsp;&nbsp;..&nbsp;.*#@@/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,%@@@@@@@@@@@@@&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,%((&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;*.&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;,&(/%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.#@@@@@@@@@@@@@@@@@@&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,%((.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,*&nbsp;*,**,#..%&nbsp;&nbsp;&nbsp;&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%@@@@@@@@@@@@@@@%.,(##@#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.%((.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%&nbsp;,*.&nbsp;&nbsp;,,&nbsp;/%*//&.%@@@@@@@@@@@@@@%.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.&.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%((.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,*&nbsp;&nbsp;&nbsp;*.&nbsp;%,&nbsp;&nbsp;.&*@@@@@@@@@@@@@@%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.@&nbsp;%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%((,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/.&nbsp;&nbsp;&nbsp;&nbsp;.(&#&nbsp;&nbsp;#@@@@@@@@@@@@@*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/@.&nbsp;#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%((,&nbsp;#(*,,.,..,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@@@@@&%(*,.&nbsp;&nbsp;&nbsp;,@@@@@@@@@@@@/&nbsp;&nbsp;&nbsp;.&*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.&nbsp;.@@@@.#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&((/*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#@#((((((#%@@@&nbsp;*@@@@@@@@@@@(.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@@@@@&/#@@@@,%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...&(/.#/,.&nbsp;.#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.@@@##%&@@@@@,&nbsp;&nbsp;&nbsp;@@@@@@@@@&((*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@@@@@@,&nbsp;@@@@,*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%.&nbsp;&nbsp;&nbsp;&nbsp;&(/*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&@@@@@@@@@@(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(@@@@@@@@((((&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#@@@@@./&nbsp;(/*%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%&nbsp;&nbsp;**.&nbsp;&nbsp;&(/**&nbsp;&nbsp;*%%.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.@@@@@@@@@@&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%@@@@@@@@(((((.&nbsp;&nbsp;&nbsp;&nbsp;.(/.,,@*&nbsp;&nbsp;,#&&(.&nbsp;&nbsp;&nbsp;&nbsp;%*//,*&nbsp;,.&(/(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/@@@@@@@@@*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*@@@&nbsp;.@@@&((((#*&nbsp;&nbsp;&nbsp;*#.&nbsp;&*&nbsp;&nbsp;*&(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;&nbsp;,.&nbsp;&nbsp;&&nbsp;(@(/(/&#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%@@@@@@@@@@@@@%.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#@@&nbsp;&nbsp;&nbsp;&@@@##((###,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%&nbsp;&nbsp;&nbsp;&nbsp;.&nbsp;&&nbsp;&nbsp;&nbsp;%(/(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&@@@@@@@@@@@@@@@@@@@&/&nbsp;&nbsp;.@&nbsp;&nbsp;&nbsp;&nbsp;@@@@#(((.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&nbsp;&nbsp;(&&nbsp;,(&nbsp;.(,.,&nbsp;&nbsp;**&&#%(/#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*@&&nbsp;&nbsp;&nbsp;.@@@&nbsp;&&nbsp;&nbsp;&nbsp;,&nbsp;&nbsp;&nbsp;#.&nbsp;%(/#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.*/(#%&&@@@@@@@@@@&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*.(@/&nbsp;&nbsp;&nbsp;@@#@@*%%&nbsp;&nbsp;&nbsp;*,&nbsp;&nbsp;&nbsp;%(/#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&@@@@@@@@@&,&nbsp;#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&nbsp;&nbsp;(#&nbsp;&nbsp;&nbsp;@@@(#@@/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%#/%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&@@@@@@@@@@#&nbsp;&nbsp;&nbsp;&nbsp;./&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/.&nbsp;&nbsp;&nbsp;&nbsp;.@@@@(((@@*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;((/%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/@@@@@@@@@@@@%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@&.&nbsp;&nbsp;&nbsp;*@@@@@@&@@@&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(#/%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&@@@@@@@@@@@@&.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/@@@@@*%@@@@@@@@@&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/#/%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.@@@@@@@@@@@@@/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%&nbsp;*@@@@@@@@@@@&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*#/&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*@@@@@@@&.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*,&nbsp;&nbsp;&nbsp;&nbsp;@@@@@@@(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*#/&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%@@@@@&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#@@,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,#/&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@@@@@@@(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&(.&nbsp;&nbsp;,.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.#/%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/@@@@@@@@*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/#&&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@@@@@@@@@@.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,%%&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,@@@@@@@@@@%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%&&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&@@@@@@@@@@@/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.%&&/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*@@@@@@@@@@&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&&&.&nbsp;.##&&&&*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.@@@@@@@@@&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#%#%#%&%#(%%.&%/%%#&&#(#&&&&@%.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*@@@@&*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.@@@@@@@@@/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%&%&&&&nbsp;*#&#((%/&/%&%*&&&%(&&&&%%&%%&#*.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%@@@@@@@@&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*@@@@@@@@@@&nbsp;*@@@(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&#%(##&&&&%&&&&&%#&nbsp;./#&&%%&&#%##%%&&&&&&%(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@@@@@@*&nbsp;%@@@(,%@@@&nbsp;&nbsp;.&@@@@@@@@@@(&nbsp;(@@@@@@,&nbsp;&nbsp;@@@@@&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*%#*&nbsp;&nbsp;.,.%%&&%*%&%*/#/&/&&%&&&%/%&&&&&&&#((%@@%###%&%&&#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*@@@@@@@*&nbsp;@@@.&nbsp;#@.&nbsp;&@@@@@@@@@@@@,&nbsp;&nbsp;@*&nbsp;&@@@&&nbsp;@,#@@@.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&&#(&###&%,(%&&&*#(*%&&&&&&&&*/&&%%#%&&&%%%&###&%&&#/&&*,#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '#@@@@@&&nbsp;&nbsp;%@@@/&nbsp;&nbsp;&nbsp;&nbsp;.@@@@&@@@@@@@@@@@@@@@,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%@@@@.&nbsp;/@@@@(.%@@@@@&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&&#&&&#(&&#,&&&&/&&&(&&/%&&%%(%&&&%%%&%&#%&&&%*&%&(%&nbsp;&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;,&%%*&#&&#*%&&%**,%%&&&&#**#&&&.#(&&&%&&&&&*%&&(&&nbsp;#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&%#&&&&%&%&&#%&&%.&nbsp;&nbsp;#&&&&&%&%%&&#%&&&(&&&&,&nbsp;&&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&&&@&*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&&&%%&&&&,*%&nbsp;.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.*,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;_______&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______&nbsp;&nbsp;&nbsp;______&nbsp;&nbsp;&nbsp;________&nbsp;&nbsp;&nbsp;__&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;______&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_______&nbsp;&nbsp;_&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '(_______)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(____&nbsp;&nbsp;\&nbsp;(_____&nbsp;\&nbsp;(_______/&nbsp;&nbsp;/&nbsp;/&nbsp;&nbsp;&nbsp;&nbsp;(_____&nbsp;\&nbsp;&nbsp;&nbsp;&nbsp;(_______)(_)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
        yield '&nbsp;_____&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;____&nbsp;&nbsp;&nbsp;____&nbsp;&nbsp;____&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;____)&nbsp;&nbsp;)&nbsp;_____)&nbsp;)&nbsp;&nbsp;&nbsp;____&nbsp;&nbsp;&nbsp;/&nbsp;/____&nbsp;&nbsp;_____)&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;_____&nbsp;&nbsp;&nbsp;&nbsp;_&nbsp;&nbsp;____&nbsp;&nbsp;&nbsp;&nbsp;____&nbsp;&nbsp;____&nbsp;&nbsp;&nbsp;&nbsp;____&nbsp;&nbsp;&nbsp;____&nbsp;<br>'
        yield '|&nbsp;&nbsp;___)&nbsp;&nbsp;&nbsp;/&nbsp;_&nbsp;&nbsp;|&nbsp;/&nbsp;___)|&nbsp;&nbsp;&nbsp;&nbsp;\&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;__&nbsp;&nbsp;(&nbsp;(_____&nbsp;(&nbsp;&nbsp;&nbsp;(___&nbsp;\&nbsp;|___&nbsp;&nbsp;&nbsp;_)|&nbsp;&nbsp;____/&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;___)&nbsp;&nbsp;|&nbsp;||&nbsp;&nbsp;_&nbsp;\&nbsp;&nbsp;/&nbsp;_&nbsp;&nbsp;||&nbsp;&nbsp;_&nbsp;\&nbsp;&nbsp;/&nbsp;___)&nbsp;/&nbsp;_&nbsp;&nbsp;)<br>'
        yield '|&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(&nbsp;(&nbsp;|&nbsp;||&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;|&nbsp;|&nbsp;|&nbsp;_&nbsp;|&nbsp;|__)&nbsp;&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;|&nbsp;_____)&nbsp;)&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;|&nbsp;&nbsp;|&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_&nbsp;|&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;||&nbsp;|&nbsp;|&nbsp;|(&nbsp;(&nbsp;|&nbsp;||&nbsp;|&nbsp;|&nbsp;|(&nbsp;(___&nbsp;(&nbsp;(/&nbsp;/&nbsp;<br>'
        yield '|_|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\_||_||_|&nbsp;&nbsp;&nbsp;&nbsp;|_|_|_|(_)|______/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|_|(______/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|_|&nbsp;&nbsp;|_|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(_)|_|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|_||_|&nbsp;|_|&nbsp;\_||_||_|&nbsp;|_|&nbsp;\____)&nbsp;\____)<br>'
        yield '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>'
         
        yield '<link rel="stylesheet" type="text/css" href="/static/style.css">'
        yield '%s<br>\n' % '==========================================='
        yield '%s <br>\n' % 'RAKE MOON LOCKER BURNS by DirtNasty'
        yield '<a href="https://farm.br34p.finance/">https://farm.br34p.finance/</a> <br>\n'
        yield '%s<br>\n' % 'RAKE Price: {} - BR34P Price: {}'.format(formatDollar(rakePrice), formatDollar(br34pPrice))
        yield '%s<br>\n' % '==========================================='
       
        for each in moonVaults:
        
            while True:
                try:
                    saveTable = getTransfers(each['add'], 'RAKE', 1e18)
                    time.sleep(1)
                    br34pTable = getTransfers(each['add'], 'BR34P', 1e8)
                except:
                    continue
                else:
                
                    saveTable['fromTroken'] = each['name']
                    df = df.append((saveTable), ignore_index=True)
                    
                    tokenCount = float(bsc.get_acc_balance_by_token_contract_address(contract_address=each['contract'], address=each['add'])) / 1e18
                    tokenPrice = geckoPrice(each['name'])

                    dollRemain.append(tokenCount * float(tokenPrice))
                    dollarAmount = formatDollar(tokenCount * float(tokenPrice))

                    
                    br34pTable['fromTroken'] = each['name']
                    br34p = br34p.append((br34pTable), ignore_index=True)

                    saveTable['timeStamp'] = pd.to_datetime(saveTable['timeStamp'],unit='s')
                    now  = datetime.utcnow()
                    duration = now - max(saveTable['timeStamp'])
                    duration_in_s = duration.total_seconds()
                    days    = divmod(duration_in_s, 86400)
                    hours   = divmod(days[1], 3600)               
                    minutes = divmod(hours[1], 60)

                    yield '<br>\n'
                    yield '<div id="item">'
                    yield '<h2>Burned token: <em>%s</em></h2><br>' % each['name']
                    yield '%s<br>\n' % ('<h3>RAKE Burned&nbsp;&nbsp;:</h3> <em>' + str(saveTable['adjustedValue'].sum()) + '</em> | Last - <em>{}</em> '.format( saveTable.loc[saveTable['timeStamp'] == max(saveTable['timeStamp']), 'adjustedValue'].sum() ))
                    yield '<h3>BR34P Burned&nbsp;:</h3>%s<br>\n' % (' <em>' + str(br34pTable['adjustedValue'].sum()) + '</em> | Last - <em>{}</em> '.format(br34pTable.loc[br34pTable['timeStamp'] == max(br34pTable['timeStamp']), 'adjustedValue'].sum() ))
                    yield '<h3>Remaining&nbsp;&nbsp;&nbsp;&nbsp;: </h3> <em>%s</em><br>\n' % (dollarAmount)
                    yield '<h3>Tx Total</h3> %s<br>\n' % (' <em>' + str(saveTable.shape[0]) + '</em>  <h3>Last Tx - <em>%d</em> days, <em>%d</em> hours, <em>%d</em> minutes ago</h3>' % (days[0], hours[0], minutes[0]))
                    yield '</div><hr>'
                    time.sleep(.1)
                    break
        dollRemain = formatDollar(sum(dollRemain))
        df['timeStamp'] = pd.to_datetime(df['timeStamp'],unit='s')
        br34p['timeStamp'] = pd.to_datetime(br34p['timeStamp'],unit='s')
        now  = datetime.utcnow()
        duration = now - max(df['timeStamp'])
        duration_in_s = duration.total_seconds()
        days    = divmod(duration_in_s, 86400)
        hours   = divmod(days[1], 3600)               
        minutes = divmod(hours[1], 60)                              

        twentyFour = now - timedelta(hours=24)
        rakex = df.loc[df['timeStamp'] >= twentyFour]
        br34px = br34p.loc[br34p['timeStamp'] >= twentyFour]
         
        yield '<br>\n'
        yield '%s<br>\n' % '=============================='
        yield '<h2>%s</h2><br>\n' % 'TOTALS'
        yield '%s<br>\n' % '=============================='
        yield '<h3>Total Transactions &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:</h3> %s<br>\n' % ('<em>' + str(df.shape[0]) + "</em> | Last Tx - <em>%d</em> days, <em>%d</em> hours, <em>%d</em> minutes ago" % (days[0], hours[0], minutes[0]))
        yield '<h3>RAKE Burned Total/USD/24h &nbsp;:</h3> %s<br>\n' % ('<em>'  + formatClean(df['adjustedValue'].sum()) + "</em> / <em> {}</em>".format(formatDollar(df['adjustedValue'].sum() * rakePrice )) + " / <em>{}</em>".format(formatClean((rakex['adjustedValue'].sum()))))  
        yield '<h3>BR34P Burned Total/USD/24h :</h3> %s<br>\n' % ('<em>' + formatClean(br34p['adjustedValue'].sum()) + ("</em> / <em>{}</em>".format(formatDollar(br34p['adjustedValue'].sum() * br34pPrice ) )) + " / <em>{}</em>".format(formatClean(br34px['adjustedValue'].sum())))
        yield '<h3>Total Remaining Balance&nbsp&nbsp;&nbsp; :</h3> <em>%s</em><br>\n' % (' ' + dollRemain)
        yield '</div>'

    return Response(getPools(), mimetype='text/html')
