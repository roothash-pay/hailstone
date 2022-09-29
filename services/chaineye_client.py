# encoding=utf-8

import grpc
from django.conf import settings
from services.savour_rpc import chaineye_pb2_grpc, chaineye_pb2


class ChaineyeClient:
    def __init__(self):
        options = [
            ('grpc.max_receive_message_length', settings.GRPC_MAX_MESSAGE_LENGTH),
        ]
        channel = grpc.insecure_channel(settings.CHAINEYE_GRPC_CHANNEL_URL, options=options)
        self.stub = chaineye_pb2_grpc.ChaineyeServiceStub(channel)

    def get_arcticle_list(self, type: str, page:int, page_size:int, consumer_token: str = None)-> chaineye_pb2.ArticleListRep:
        return self.stub.getArticleList(
            chaineye_pb2.ArticleListRep(
                consumer_token=consumer_token,
                type=type,
                page=page,
                pagesize=page_size,
            )
        )

    def get_arcticle_detail(self, type:str, id:int, consumer_token: str = None) -> chaineye_pb2.ArticleDetailRep:
        return self.stub.getArticleDetail(
            chaineye_pb2.ArticleDetailReq(
                consumer_token=consumer_token,
                type=type,
                id=id
            )
        )

    def get_comment_list(self, article_id:int, page:int, page_size:int, consumer_token: str = None) -> chaineye_pb2.CommentListRep:
        return self.stub.getCommentList(
            chaineye_pb2.CommentListReq(
                consumer_token=consumer_token,
                article_id=article_id,
                page=page,
                pagesize=page_size,
            )
        )

    def get_like_address(self, author_id:int, consumer_token: str = None)->chaineye_pb2.AddressRep:
        return self.stub.getLikeAddress(
            chaineye_pb2.AddressReq(
                consumer_token=consumer_token,
                author_id=author_id
            )
        )

    def like_article(
            self,
            tx_hash:str,
            like_from:str,
            like_to: str,
            amount:str,
            asset_name: str,
            token_address: str,
            consumer_token: str = None
    )->chaineye_pb2.LikeRep:
        return self.stub.likeArticle(
            chaineye_pb2.LikeReq(
                consumer_token=consumer_token,
                tx_hash=tx_hash,
                like_from=like_from,
                like_to=like_to,
                amount=amount,
                asset_name=asset_name,
                token_address=token_address
            )
        )
