#encoding=utf-8

import json
from typing import Any, Dict, List, Optional, Union
from services.savour_rpc import chaineye_pb2


class Article:
    article: chaineye_pb2.ArticleListRep

    def __init__(self, article):
        self.article = article

    def as_json(self, type)-> Dict[str, Any]:
        return {
            "id": self.article.id,
            "title": self.article.title,
            "type": type,
            "image": self.article.cover,
            "abstract": self.article.abstract,
            "author": self.article.author,
            "add_time": self.article.add_time,
            "upd_time": self.article.upd_time,
        }


class ArticleDetail:
    article: chaineye_pb2.ArticleDetailRep

    def __init__(self, article):
        self.article = article

    def as_json(self) -> Dict[str, Any]:
        return {
            "title": self.article.title,
            "detail": self.article.detail,
            "author_id": self.article.author_id,
            "author": self.article.author,
            "views": self.article.views,
            "like": self.article.like,
            "add_time": self.article.add_time,
            "upd_time": self.article.upd_time,
            "comments": [],
            "likes": [],
        }


class Comment:
    def __init__(self):
        pass

    def from_json(data: Dict[str, Any]) -> "Comment":
        pass

    def as_json(self) -> Dict[str, Any]:
        pass
