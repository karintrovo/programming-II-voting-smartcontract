""" Utility functions and shortcuts for the WSC winter school
    (c) 2022 peter.gruber@usi.ch
    (c) 2022 travad@usi.ch
"""
    
from typing import Dict


def load_credentials(file_name: str = "credentials") -> Dict:
    """
        Given the filename in which credentials were store, 
        it loads them from memory
    """
    import os, json
    from pathlib import Path

    credential_path = (Path( os.curdir ) / ".." / "assets" / "credentials" / file_name ).resolve()
    
    # make sure the file exists, otherwise throw an exception
    if credential_path.exists():

        with open(credential_path, 'r') as json_file:
            cred = json.load(json_file)
        return(cred)

    else:

        raise Exception("No credential file found. Make sure to run 01-members-credentials before moving on")


def generate_account_dict():
    from algosdk import account, mnemonic
    import random
    private_key = account.generate_account()[0]    # need [0], because generate_account() returns a list
    acc = {}
    acc['public'] = account.address_from_private_key(private_key)
    acc['private'] = private_key
    acc['mnemonic'] = mnemonic.from_private_key(private_key)
    return acc


def send_payment(algod_client, sender_private, receiver_public, amount, note=''):
    # algod_client = algosdk client
    # sender_private = private key of sender
    # receiver_public = public address of sender
    # amount = amount in ALGOs
    # note = note as encoded JSON (if any)
    from algosdk import account
    from algosdk.v2client import algod
    from algosdk.future.transaction import PaymentTxn
   
    sp             = algod_client.suggested_params()
    algo_precision = 1e6
    sender_public  = account.address_from_private_key(sender_private)
    amount_microalgo = int(amount * algo_precision)

    unsigned_txn = PaymentTxn(sender_public, sp, receiver_public, amount_microalgo, None, note)
    
    signed_txn = unsigned_txn.sign(sender_private)
    txid = algod_client.send_transaction(signed_txn)
    return(txid)


def wait_for_confirmation(algod_client, txid):
    # algod_client = algosdk client
    # txid = transaction ID, for example from send_payment()
    
    # TODO: improve to work with groups
    from algosdk import account
    from algosdk.v2client import algod
    
    if txid is None:
        print("Empty transaction id.")
        return None
    else:
        current_round = algod_client.status()["last-round"]        # obtain last round number
        print("Current round is  {}.".format(current_round))
        txinfo = algod_client.pending_transaction_info(txid)       # obtain transaction information
   
        # Wait for confirmation
        while ( txinfo.get('confirmed-round') is None ):            # condition for waiting = 'confirmed-round' is empty
            print("Waiting for round {} to finish.".format(current_round))
            algod_client.status_after_block(current_round)             # this wait for the round to finish
            txinfo = algod_client.pending_transaction_info(txid)    # update transaction information
            current_round += 1

        print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
        return txinfo

    # helper function that waits for a given txid to be confirmed by the network
def wait_for_confirmation_t(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))
    
def note_encode(note_dict):
    import json
    # note dict ... a Python dictionary
    note_json = json.dumps(note_dict)
    note_byte = note_json.encode()     
    return(note_byte)

def note_decode(note_64):
    # note64 =  note in base64 endocing
    # returns a Python dict
    import base64
    
    message_base64 = txinfo['txn']['txn']['note']
    message_byte   = base64.b64decode(message_base64)
    message_json   = message_byte.decode()
    message_dict   = json.loads( message_json )
    return(message_dict)

def asset_holdings(algod_client, public):
    # algod_client = algosdk client
    # public = public address to be analyzed

    import pandas as pd
    from algosdk.v2client import algod
    account_info = algod_client.account_info(public)

    info = []
    # Algo part
    info.append( {'amount':  account_info['amount']/1E6, 
                  'unit' :   'ALGO', 
                  'asset-id': 0, 
                  'name': 'Algorand',
                  'decimals': 6
                  } )

    # ASA part
    assets = account_info['assets']
    for asset in assets:
        asset_id     = asset['asset-id']
        asset_info   = algod_client.asset_info(asset_id)                         # Get all info
        asset_amount = asset['amount']/10**asset_info['params']['decimals']      # convert to BIG units
        asset_unit   = asset_info['params']['unit-name']
        info.append( {'amount':  asset_amount,
                      'unit' :   asset_unit,
                      'asset-id':asset_id,
                      'name': asset_info['params']['name'],
                      'decimals': asset_info['params']['decimals']
                      } )
    return(info) #.sort_values('asset-id')



def asset_holdings_df(algod_client, public):
    # algod_client = algosdk client
    # public = public address to be analyzed

    import pandas as pd
    from algosdk.v2client import algod
    info = asset_holdings(algod_client, public)
    df = pd.DataFrame(info)
    return(df)


def asset_holdings_df2(algod_client,adr1,adr2,suffix=['','']):
    # algod_client = algosdk client
    # adr1, adr2 = public address to be analyzed
    import pandas as pd
    from algosdk.v2client import algod
    info1 = asset_holdings(algod_client, adr1)
    df1 = pd.DataFrame(info1)
    info2 = asset_holdings(algod_client, adr2)
    df2 = pd.DataFrame(info2)
    pd.set_option('precision', 4)
    df_merge = pd.merge(df1,df2,how="outer", on=["asset-id", "unit", "name", "decimals"],suffixes=suffix)
    return(df_merge)

def read_local_state(client, addr, app_id):
    # reads a user's local state
    # client = algod_client
    # addr = public addr of the user that we want to inspect
    results = client.account_info(addr)
    for local_state in results["apps-local-state"]:
        if local_state["id"] == app_id:
            if "key-value" not in local_state:
                return {}
            return format_state(local_state["key-value"])
    return {}

def read_global_state(client, app_id):
    # reads an app's global state
    return client.application_info(app_id)["params"]["global-state"]

def format_state(state):
    import base64
    # formats the state (local/global) nicely 
    formatted = {}
    textvariables = {'Winner', 'VoteInfo'}      # we are interested to know the winner
    for item in state:
        key = base64.b64decode(item["key"]).decode("utf-8")
        value = item["value"]
        if value["type"] == 1:
            if key in textvariables:                 # Format text variables
                formatted_value = base64.b64decode(value["bytes"]).decode("utf-8")
            else:                                    # Format addresses
                formatted_value = base64.b32encode(base64.b64decode(value["bytes"]))
            formatted[key] = formatted_value
        else:
            formatted[key] = value["uint"]
    return formatted

