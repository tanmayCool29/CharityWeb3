from flask import Flask, render_template, request, redirect, url_for
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account import Account
import json
from math import ceil

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

# Connect to Ganache
web3 = Web3(HTTPProvider('http://localhost:8545'))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load contract ABI
with open('build/contracts/CharityWebsite.json', 'r') as f:
    contract_data = json.load(f)
contract_abi = contract_data['abi']
contract_address = '0xFF86C862846b81520eD14F57E808B6E2B7A76ef3'  
charity_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    
    num_projects = charity_contract.functions.getNumCharityProjects().call()
    projects = []
    for i in range(num_projects):
        project = charity_contract.functions.getCharityProject(i).call()
        projects.append(project)
    return render_template('index.html', projects=projects)

@app.route('/create_charity', methods=['GET', 'POST'])
def create_charity():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        target_amount = int(request.form['targetAmount'])
        wallet_address = request.form['walletAddress']
        
        # Perform contract interaction
        gas_price = int(web3.eth.gas_price)  # Convert to integer
        gas_limit = 2000000
        nonce = web3.eth.get_transaction_count(web3.eth.accounts[0])
        
        tx_data = charity_contract.encodeABI(fn_name='createCharityProject', args=[title, description, target_amount, wallet_address])
        tx_dict = {
            'chainId': 1,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': nonce,
            'to': contract_address,
            'data': tx_data,
        }

        # private_key = '0xe96a43fe7e73fcfefb9cf5922209b8645ab16de50f6128b25d08a273c2754794'
        private_key = '0x3f88e6d4fd529e0c31e5de6c715323158e6006941d59d9e0a3677c5d2128bb21'
        signed_tx = web3.eth.account.sign_transaction(tx_dict, private_key)
        # signed_tx = Account.signTransaction(tx_dict, private_key)
        tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return render_template('index.html')
    else:
        return render_template('create_charity.html')
    

@app.route('/all_charities')
def all_charities():
    num_projects = charity_contract.functions.getNumCharityProjects().call()
    projects = [charity_contract.functions.getCharityProject(i).call() for i in range(num_projects)]

    cnt = 1
    id = 0

    for i in range(len(projects)):
        print("\n")
        arr = projects[i]
        arr.append(str(cnt)+'.jpg')
        arr.append(id)
        id+=1
        cnt+=1
        cnt%=10
        print(projects[i])
        print("\n-----------\n")

    num_groups = ceil(num_projects / 3)

    # print(f"num_groups:{num_groups}")

    # grouped_projects = []
    # i = 0
    # while(i<len(projects)):
    #     grp = []
    #     j = 0
    #     while(i<len(projects) and j<3):
    #         grp.append(projects[i])
    #         j+=1
    #         i+=1
    #     grouped_projects.append(grp)
    #     print(grp)
    #     print("\n----------------\n")
    # print(grouped_projects)


    grouped_projects = [projects[i:i+3] for i in range(0, num_projects, 3)]

    print(grouped_projects)
    return render_template('all_charities.html', grouped_projects=grouped_projects)


@app.route('/donate/<int:project_id>', methods=['GET'])
def donate(project_id):
    return render_template('donate.html', project_id=project_id)

@app.route('/donate/<int:project_id>', methods=['POST'])
def donate_post(project_id):
    if request.method == 'POST':
        amount = int(request.form['flexRadioDefault'])
        
        # Perform donation transaction
        gas_price = int(web3.eth.gas_price)
        gas_limit = 2000000
        nonce = web3.eth.get_transaction_count(web3.eth.accounts[0])
        
        tx_data = charity_contract.encodeABI(fn_name='donate', args=[project_id, amount])
        tx_dict = {
            'chainId': 1,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': nonce,
            'to': contract_address,
            'data': tx_data,
        }

        # private_key = '0xe96a43fe7e73fcfefb9cf5922209b8645ab16de50f6128b25d08a273c2754794'
        private_key = '0x3f88e6d4fd529e0c31e5de6c715323158e6006941d59d9e0a3677c5d2128bb21'
        signed_tx = web3.eth.account.sign_transaction(tx_dict, private_key)
        tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print("\n\nDonated money !\n\n")

        return redirect(url_for('index'))
    

@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/news_detail')
def news_detail():
    return render_template('news-detail.html')


    

if __name__ == "__main__":
    app.run(host='0.0.0.0')