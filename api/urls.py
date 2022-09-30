# encoding=utf-8

from django.urls import path
from api.wallet.hd_api_v1 import (
    get_balance,
    get_wallet_balance,
    get_nonce,
    get_account_info,
    get_fee,
    send_transaction,
    get_unspend_list,
    get_hash_transaction,
    get_address_transaction,
    submit_wallet_info,
    batch_submit_wallet,
    delete_wallet,
    get_note_book,
    add_note_book,
    del_note_book,
    upd_note_book
)

import api.market.api_v1 as market

urlpatterns = [
    # Hd wallet module
    path(r'get_balance', get_balance, name='get_balance'),
    path(r'get_wallet_balance', get_wallet_balance, name='get_wallet_balance'),
    path(r'get_nonce', get_nonce, name='get_nonce'),
    path(r'get_account_info', get_account_info, name='get_account_info'),
    path(r'get_fee', get_fee, name='get_fee'),
    path(r'send_transaction', send_transaction, name='send_transaction'),
    path(r'get_unspend_list', get_unspend_list, name='get_unspend_list'),
    path(r'get_hash_transaction', get_hash_transaction, name='get_hash_transaction'),
    path(r'get_address_transaction', get_address_transaction, name='get_address_transaction'),
    path(r'submit_wallet_info', submit_wallet_info, name='submit_wallet_info'),
    path(r'batch_submit_wallet', batch_submit_wallet, name='batch_submit_wallet'),
    path(r'delete_wallet', delete_wallet, name='delete_wallet'),
    path(r'get_note_book', get_note_book, name='get_note_book'),
    path(r'add_note_book', add_note_book, name='add_note_book'),
    path(r'upd_note_book', upd_note_book, name='upd_note_book'),
    path(r'del_note_book', del_note_book, name='del_note_book'),

    # market module
    path(r'get_exchanges', market.get_exchanges, name='get_exchanges'),
    path(r'get_assets', market.get_assets, name='get_assets'),
    path(r'get_stable_coins', market.get_stable_coins, name='get_stable_coins'),
    path(r'get_stable_coin_price', market.get_stable_coin_price, name='get_stable_coin_price'),
    path(r'get_symbols', market.get_symbols, name='get_symbols'),
    path(r'get_symbol_prices', market.get_symbol_prices, name='get_symbol_prices'),

    # chaineye module

]