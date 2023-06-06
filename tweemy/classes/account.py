import tweemy.config
import json
import requests


class Account:
    """Class to manage your account"""

    def login_by_cookies_and_headers(self, cookies: dict, headers: dict):
        """
        Login using cookies and headers
        Parameters
        ----------
        cookies: dict
            cookies
        headers: dict
            headers
        Returns
        -------
        None
        """

        tweemy.config.cookies = cookies
        tweemy.config.headers = headers

    def get_settings(self) -> dict:
        """
        Fetch account settings.

        Returns
        -------
        Dict
        """
                
        response = requests.get(
            'https://api.twitter.com/1.1/account/settings.json?include_mention_filter=true&include_nsfw_user_flag=true&include_nsfw_admin_flag=true&include_ranked_timeline=true&include_alt_text_compose=true&ext=ssoConnections&include_country_code=true&include_ext_dm_nsfw_media_filter=true&include_ext_sharing_audiospaces_listening_data_with_followers=true',
            cookies = tweemy.config.cookies,
            headers=tweemy.config.headers
        )

        return json.loads(response.text)

    def get_info(self) -> dict:
        """
        Fetch account info.

        Returns
        -------
        Dict
        """

        params = {
            'variables': '{"screen_name":"username","withSafetyModeUserFields":true}'.replace('username', self.get_settings()['screen_name']),
            'features': '{"hidden_profile_likes_enabled":false,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
        }

        response = requests.get(
            'https://twitter.com/i/api/graphql/XA6F1nJELYg65hxOC2Ekmg/UserByScreenName',
            params=params,
            cookies=tweemy.config.cookies,
            headers=tweemy.config.headers,
        )

        return json.loads(response.text)['data']['user']['result']

    def edit_profile(self, full_name: str = "", description: str = "", external_url: str = "") -> dict:
        """
        Edit information of profile
        Parameters
        ----------
        full_name: str
            Full name
        description: str
            Description of account
        Returns
        -------
        Dict
        """

        payload = {'name': full_name, 'description': description, 'url': external_url}

        response = requests.post('https://api.twitter.com/1.1/account/update_profile.json', data=payload, cookies=tweemy.config.cookies, headers=tweemy.config.headers)

        return json.loads(response.text)

    def write_message(self, user_id: int, message_text: str) -> dict:
        """
        Write message to user

        Returns
        -------
        Dict
        """

        payload = '{"conversation_id":"user_id-my_id","recipient_ids":false,"request_id":"255d1270-0452-11ee-942a-7bba27d2c6c1","text":"message_text","cards_platform":"Web-12","include_cards":1,"include_quote_count":true,"dm_users":false}'.replace(
                    'user_id', str(user_id)).replace(
                    'message_text', message_text).replace(
                    'my_id', str(self.get_info()['rest_id']))

        response = requests.post(
            'https://twitter.com/i/api/1.1/dm/new2.json?ext=mediaColor^%^2CaltText^%^2CmediaStats^%^2ChighlightedLabel^%^2ChasNftAvatar^%^2CvoiceInfo^%^2CbirdwatchPivot^%^2Cenrichments^%^2CsuperFollowMetadata^%^2CunmentionInfo^%^2CeditControl&include_ext_alt_text=true&include_ext_limited_action_results=false&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_groups=true&include_inbox_timelines=true&include_ext_media_color=true&supports_reactions=true',
            cookies=tweemy.config.cookies,
            headers=tweemy.config.headers,
            data=payload,
        )

        return response.text
