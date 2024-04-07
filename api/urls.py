# encoding=utf-8

from django.urls import path

from api.wallet.social_wallet_api_v1 import (
    get_head,
    save_head,
    get_recovery_key,
    set_recovery_key,
)
from api.wallet.token_api_v1 import (
    get_tokens,
)
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
    delete_wallet_token,
    get_note_book,
    add_note_book,
    del_note_book,
    upd_note_book,
    hot_token_list,
    sourch_add_token,
    get_wallet_asset,
    get_sign_tx_info,
    update_wallet_name,
)

from api.market.api_v1 import (
    get_exchanges,
    get_exchange_market,
    get_market_detail,
    add_favorite_market,
    remove_favorite_market
)

from api.circle.api_v1 import (
    get_cat_list,
    get_like_address,
    get_comment_list,
    get_arcticle_list,
    get_arcticle_detail,
    like_article
)
from api.airdrop.api_v1 import (
    get_points_by_address,
    get_points_record_by_address,
    get_invite_code_by_address,
    submit_invite_info,
    get_project_interactions,
    get_questions,
    get_reward_info
)
from api.website.api_v1 import (
    get_blog_list,
    get_event_list,
    get_forum_list,
    get_blog_cat_list
)

from api.l3staking.api_v1 import (
    get_staking_chains,
    get_staking_node_list,
    get_node_detail
)


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
    path(r'delete_wallet_token', delete_wallet_token, name='delete_wallet_token'),
    path(r'get_note_book', get_note_book, name='get_note_book'),
    path(r'add_note_book', add_note_book, name='add_note_book'),
    path(r'upd_note_book', upd_note_book, name='upd_note_book'),
    path(r'del_note_book', del_note_book, name='del_note_book'),
    path(r'hot_token_list', hot_token_list, name='hot_token_list'),
    path(r'sourch_add_token', sourch_add_token, name='sourch_add_token'),
    path(r'get_wallet_asset', get_wallet_asset, name='get_wallet_asset'),
    path(r'get_sign_tx_info', get_sign_tx_info, name='get_sign_tx_info'),
    path(r'update_wallet_name', update_wallet_name, name='update_wallet_name'),

    # market module
    path(r'get_exchanges', get_exchanges, name='get_exchanges'),
    path(r'get_exchange_market', get_exchange_market, name='get_exchange_market'),
    path(r'get_market_detail', get_market_detail, name='get_market_detail'),
    path(r'add_favorite_market', add_favorite_market, name='add_favorite_market'),
    path(r'remove_favorite_market', remove_favorite_market, name='remove_favorite_market'),

    # chaineye module
    path(r'get_cat_list', get_cat_list, name='get_cat_list'),
    path(r'get_like_address', get_like_address, name='get_like_address'),
    path(r'get_comment_list', get_comment_list, name='get_comment_list'),
    path(r'get_arcticle_list', get_arcticle_list, name='get_arcticle_list'),
    path(r'get_arcticle_detail', get_arcticle_detail, name='get_arcticle_detail'),
    path(r'like_article', like_article, name='like_article'),

    # wallet head module
    path(r'get_head', get_head, name='get_head'),
    path(r'save_head', save_head, name='save_head'),
    path(r'get_recovery_key', get_recovery_key, name='get_recovery_key'),
    path(r'set_recovery_key', set_recovery_key, name='set_recovery_key'),
    path(r'get_tokens', get_tokens, name='get_tokens'),

    # airdrop
    path(r'get_reward_info', get_reward_info, name='get_reward_info'),
    path(r'get_project_interactions', get_project_interactions, name='get_project_interactions'),
    path(r'get_questions', get_questions, name='get_questions'),
    path(r'get_invite_code_by_address', get_invite_code_by_address, name='get_invite_code_by_address'),
    path(r'submit_invite_info', submit_invite_info, name='submit_invite_info'),
    path(r'get_points_by_address', get_points_by_address, name='get_points_by_address'),
    path(r'get_points_record_by_address', get_points_record_by_address, name='get_points_record_by_address'),

    # official website
    path(r'get_blog_cat_list', get_blog_cat_list, name='get_blog_cat_list'),
    path(r'get_blog_list', get_blog_list, name='get_blog_list'),
    path(r'get_event_list', get_event_list, name='get_event_list'),
    path(r'get_forum_list', get_forum_list, name='get_forum_list'),

    # l3staking
    path(r'get_staking_chains', get_staking_chains, name='get_staking_chains'),
    path(r'get_staking_node_list', get_staking_node_list, name='get_staking_node_list'),
    path(r'get_node_detail', get_node_detail, name='get_node_detail'),
]