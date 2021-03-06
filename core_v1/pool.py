from flask import Flask, render_template
import json
from snek.snek import SnekDB
from park.park import Park

from pathlib import Path
pool_path = Path().resolve().parent

def parse_pool():

    with open(pool_path / 'config/pool.json') as data_file:
        data = json.load(data_file)
    with open(pool_path / 'config/networks.json') as network_file:
        network = json.load(network_file)
        
    return data, network

def get_network(d, n, ip="localhost"):

    return Park(
        ip,
        n[d['network']]['port'],
        n[d['network']]['nethash'],
        n[d['network']]['version']
    )

app = Flask(__name__)

@app.route('/')
def index():    
    s = {} 
    dstats = park.delegates().delegates()
    for i in dstats['delegates']:
        if i['username'] == data['delegate']:
            pubKey = i['publicKey']
            s['forged'] = i['producedblocks']
            s['missed'] = i['missedblocks']
            s['rank'] = i['rate']
            s['productivity'] = i['productivity']
            if s['rank'] <= 201:
                s['forging'] = 'Forging'
            else:
                s['forging'] = 'Standby'

    s['votes'] = len(park.delegates().voters(pubKey)['accounts'])
    
    voter_data = snekdb.voters().fetchall()
    
    return render_template('index.html', node=s, row=voter_data, n=navbar)

@app.route('/payments')
def payments():
    
    data = snekdb.transactions().fetchall()
    tx_data=[]
    for i in data:
        l = [i[0], int(i[1]), i[2], i[3]]
        tx_data.append(l)
 
    return render_template('payments.html', row=tx_data, n=navbar)

if __name__ == '__main__':
    data, network = parse_pool()
    snekdb = SnekDB(data['dbusername'])
    park = get_network(data, network)
    navbar = {
       'dname': data['delegate'],
       'proposal': data['proposal'],
       'explorer': data['explorer'],
       'coin': data['coin']}
    
    app.run(host=data['pool_ip'])
