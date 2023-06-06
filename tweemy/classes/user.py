import tweemy.config
import json
import requests

class User:
    """Class to manage users"""
    
    def __init__(self, username: str):
        self.username = username
        self.account_info = self._get_info()

    def _get_info(self) -> dict:
        """
        Fetch user info.

        Returns
        -------
        Dict
        """
        params = {
            'variables': '{"screen_name":"username","withSafetyModeUserFields":true}'.replace('username', self.username),
            'features': '{"hidden_profile_likes_enabled":false,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
        }

        response = requests.get(
            'https://twitter.com/i/api/graphql/XA6F1nJELYg65hxOC2Ekmg/UserByScreenName',
            params=params,
            cookies=tweemy.config.cookies,
            headers=tweemy.config.headers,
        )

        return json.loads(response.text)['data']['user']['result']
