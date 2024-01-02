import logging
import tweepy
from urllib.parse import urlparse, parse_qs

from apps.quest import dao
from apps.quest.models import QuestAction, Quest
from apps.user.models import UserInfoExt
from core.utils.tool_util import find_all_indices
from settings.config import settings

logger = logging.getLogger(__name__)


async def checkTwitterFollow(userId: int, questAction: QuestAction) -> bool:
    completed = False
    userInfoExt = await UserInfoExt.filter(account_id=userId).first()
    if not userInfoExt or not userInfoExt.twitter_user_id or len(userInfoExt.twitter_user_id) == 0:
        return completed
    quest = await Quest.filter(id=questAction.quest_id, status='ongoing').first()
    if not quest:
        return completed
    # try:
    #     client = tweepy.Client(userInfoExt.twitter_access_token)
    #     response = client.get_users_following(userInfoExt.twitter_user_id)
    #     for user in response.data:
    #         if user.id == settings.TWITTER_USER_ID:
    #             completed = True
    # except tweepy.TweepyException as e:
    #     logger.error(f"checkTwitterFollow error:{e}")
    # if not completed:
    #     return completed
    completed = True
    await dao.actionCompleted(userId, questAction, quest)
    return completed


async def checkTwitterCreate(userId: int, questAction: QuestAction) -> bool:
    completed = False
    userInfoExt = await UserInfoExt.filter(account_id=userId).first()
    if not userInfoExt or not userInfoExt.twitter_access_token or len(userInfoExt.twitter_access_token) == 0:
        return completed
    quest = await Quest.filter(id=questAction.quest_id, status='ongoing').first()
    if not quest:
        return completed
    try:
        parsed_url = urlparse(questAction.source)
        query_str = parsed_url.query
        params = parse_qs(query_str)
        text = params.get("text", [None])[0]
        if text:
            eventIndices = find_all_indices(text, "#")
            eventKeys = list()
            for index in eventIndices:
                blankIndex = text.index(" ", index)
                if blankIndex > 0:
                    eventKeys.append(text[index:blankIndex])
            client = tweepy.Client(userInfoExt.twitter_access_token)
            response = client.get_users_tweets(userInfoExt.twitter_user_id, max_results=10, tweet_fields=['entities', 'text'])
            for tweet in response.data:
                if not tweet.text:
                    continue
                if not tweet.entities or not tweet.entities.get('mentions', None):
                    continue
                for mention in tweet.entities['mentions']:
                    if mention['id'] == str(settings.TWITTER_USER_ID):
                        completed = True
                        break
                if completed:
                    for key in eventKeys:
                        if key not in tweet.text:
                            completed = False
                            break
                if completed:
                    break
    except tweepy.TweepyException as e:
        logger.error(f"checkTwitterCreate error:{e}")
    if not completed:
        return completed
    await dao.actionCompleted(userId, questAction, quest)
    return completed


async def checkTwitterQuote(userId: int, questAction: QuestAction) -> bool:
    completed = False
    userInfoExt = await UserInfoExt.filter(account_id=userId).first()
    if not userInfoExt or not userInfoExt.twitter_access_token or len(userInfoExt.twitter_access_token) == 0:
        return completed
    quest = await Quest.filter(id=questAction.quest_id, status='ongoing').first()
    if not quest:
        return completed
    try:
        client = tweepy.Client(userInfoExt.twitter_access_token)
        response = client.get_users_tweets(userInfoExt.twitter_user_id, max_results=10, tweet_fields=['entities', 'referenced_tweets'])
        for tweet in response.data:
            if not tweet.referenced_tweets or not tweet.entities:
                continue
            if not tweet.entities.get('mentions', None) or len(tweet.entities['mentions']) < 3:
                continue
            for tweet in tweet.referenced_tweets:
                if tweet.id == settings.TWITTER_TWEET_ID:
                    completed = True
                    break
    except tweepy.TweepyException as e:
        logger.error(f"checkTwitterQuote error:{e}")
    if not completed:
        return completed
    await dao.actionCompleted(userId, questAction, quest)
    return completed


async def checkTwitterLike(userId: int, questAction: QuestAction) -> bool:
    completed = False
    userInfoExt = await UserInfoExt.filter(account_id=userId).first()
    if not userInfoExt or not userInfoExt.twitter_access_token or len(userInfoExt.twitter_access_token) == 0:
        return completed
    quest = await Quest.filter(id=questAction.quest_id, status='ongoing').first()
    if not quest:
        return completed
    try:
        client = tweepy.Client(userInfoExt.twitter_access_token)
        response = client.get_liked_tweets(userInfoExt.twitter_user_id, max_results=10, tweet_fields=['id'])
        for tweet in response.data:
            if tweet.id == settings.TWITTER_TWEET_ID:
                completed = True
                break
    except tweepy.TweepyException as e:
        logger.error(f"checkTwitterLike error:{e}")
    if not completed:
        return completed
    await dao.actionCompleted(userId, questAction, quest)
    return completed


async def checkTwitterRetweet(userId: int, questAction: QuestAction) -> bool:
    completed = False
    userInfoExt = await UserInfoExt.filter(account_id=userId).first()
    if not userInfoExt or not userInfoExt.twitter_access_token or len(userInfoExt.twitter_access_token) == 0:
        return completed
    quest = await Quest.filter(id=questAction.quest_id, status='ongoing').first()
    if not quest:
        return completed
    try:
        client = tweepy.Client(userInfoExt.twitter_access_token)
        response = client.get_retweeters(settings.TWITTER_TWEET_ID, max_results=100, user_fields=['id'])
        for user in response.data:
            if user.id == int(userInfoExt.twitter_user_id):
                completed = True
                break
    except tweepy.TweepyException as e:
        logger.error(f"checkTwitterRetweet error:{e}")
    await dao.actionCompleted(userId, questAction, quest)
    return completed