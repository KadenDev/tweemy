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
    
    def get_followers(self) -> list:
        """
        Fetch user followers.

        Returns
        -------
        List
        """
        
    
        for i in range(1, self.account_info['legacy']['followers_count'] // 100):
            params = {
                'variables': '{"userId":"user_id","count":100,"includePromotedContent":false}'.replace('user_id', self.account_info['rest_id']),
                'features': '{"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":false,"responsive_web_enhance_cards_enabled":false}',
            }
            
            if i != 1:
                cursor = json.loads(response.text)['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][-2]['content']['value']

                params = {
                    'variables': '{"userId":"user_id","count":100,"cursor":"cursor","includePromotedContent":false}}'.replace(
                        'user_id', self.account_info['rest_id']
                    ).replace('cursor', cursor),
                    
                    'features': '{"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":false,"responsive_web_enhance_cards_enabled":false}',
                }

            response = requests.get(
                'https://twitter.com/i/api/graphql/EAqBhgcGr_qPOzhS4Q3scQ/Followers',
                params=params,
                cookies=tweemy.config.cookies,
                headers=tweemy.config.headers,
            )

            for follower in json.loads(response.text)['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][:-2]:
                yield follower
        