import os
from dotenv import load_dotenv

def get_env(): #.envファイルに定義したdiscordbotのtokenやdiscordサーバーのサーバーid,ボイスチャンネルidを取得
    
    load_dotenv()
    print(os.path.abspath('.env'))

    discord_bot_token = os.getenv('TOKEN')
    text_channel_id = os.getenv('TEXT_CHANNEL_ID')
    team_1_voice_channel_id = os.getenv('TEAM_1_VOICE_CHANNEL_ID')
    team_2_voice_channel_id = os.getenv('TEAM_2_VOICE_CHANNEL_ID')

    if not discord_bot_token:
        raise ValueError('Please set the environment variable TOKEN.')
    if not text_channel_id:
        raise ValueError('Please set the environment variable TEXT_CHANNEL_ID.')
    if not team_1_voice_channel_id:
        raise ValueError('Please set the environment variable TEAM_1_VOICE_CHANNEL_ID .')
    if not team_2_voice_channel_id:
        raise ValueError('Please set the environment variable TEAM_2_VOICE_CHANNEL_ID .')

    return {
        'TOKEN': discord_bot_token,
        'TEXT_CHANNEL_ID': text_channel_id, 
        'TEAM_1_VOICE_CHANNEL_ID': team_1_voice_channel_id,
        'TEAM_2_VOICE_CHANNEL_ID': team_2_voice_channel_id,
    }