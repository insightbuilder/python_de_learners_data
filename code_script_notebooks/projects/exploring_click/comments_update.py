# Script that reads and writes replies to comments on youtube videos based on the yt-link
import click
import pickle
import os
from dotenv import load_dotenv
from google_auth_oauthlib import flow
from google.auth.transport.requests import Request
from googleapiclient import discovery, errors
import urllib.parse as urlparse


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

path_secret = "client_secret_insight.json"

load_dotenv('.env')
DEVELOPER_KEY = os.environ['DEV_KEY_INSIGHT']
api_service_name = "youtube"
api_version = "v3"

@click.group("YT_App")
def main():
    pass


# write the function to first extract the video id from the link
@main.command("get_link", help="Extracts the video id from the yt-link")
@click.argument("ytlink", type=click.STRING)
def get_link(ytlink):
    """
    Extracts the video ID from a YouTube URL.

    Supported patterns:
    - http://youtu.be/{video_id}
    - http://www.youtube.com/watch?v={video_id}
    - http://www.youtube.com/embed/{video_id}
    - https://youtu.be/{video_id}?si={SOME_ID}

    Args:
        url (str): A YouTube URL containing a video ID.

    Returns:
        str: The extracted video ID.
    """
    query = urlparse.urlparse(ytlink)
    if query.hostname == 'youtu.be':
        print(query.path[1:])
        return query.path[1:]
    elif query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            params = urlparse.parse_qs(query.query)
            click.echo(params['v'][0])
            return params['v'][0]
        elif query.path.startswith('/embed/'):
            click.echo(query.path.split('/')[2])
            return query.path.split('/')[2]
        elif query.path.startswith('/v/'):
            click.echo(query.path.split('/')[2])
            return query.path.split('/')[2]
    # If none of the patterns match, return None
    return None


@main.command("get_comments",
              help='Returns number of comments present, has other options')
@click.option('-n', '--num_comments', help="Get the required num of comments")
@click.argument('vidid', type=click.STRING)
def get_comments(vidid, num_comments):
    youtube_write = discovery.build(api_service_name, api_version,
                                    developerKey=DEVELOPER_KEY)
    req_list = youtube_write.commentThreads().list(
        part="snippet",
        videoId=vidid,
        maxResults=100
    )
    raw_res = req_list.execute()
    # click.echo(raw_res['items'])
    if not num_comments:
        click.echo(raw_res['pageInfo'])
        click.echo(list(raw_res.keys()))
        click.echo(len(raw_res['items']))
        click.echo(raw_res['items'][0])


@main.command('reply_comment')
@click.option('--comment_id', type=click.STRING)
@click.option('--text', type=click.STRING)
def write_comment(text, comment_id):
    your_creds = None
    # token.pickle stores the user's credentials 
    # from previously successful logins
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            your_creds = pickle.load(token)
    # If there are no valid credentials available, then either refresh the token or log in.
    if not your_creds or not your_creds.valid:
        if your_creds and your_creds.expired and your_creds.refresh_token:
            print('Refreshing Access Token...')
            your_creds.refresh(Request())
        else:
            print('Fetching New Tokens...')
            your_flow = flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file=path_secret,
                scopes=scopes)

            your_flow.run_local_server(port=8080, prompt='consent',
                                       authorization_prompt_message='')
            your_creds = your_flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(your_creds, f)
    # click.echo(your_creds.to_json())
    youtube_write = discovery.build(api_service_name, api_version,
                                    credentials=your_creds)
    # click.echo(youtube_write)
    
    resp = youtube_write.comments().insert(
        part="snippet",
        body=dict(
            snippet=dict(
                parentId=comment_id,
                textOriginal=text
                )
        )
    ).execute()
    
    click.echo(resp)

if __name__ == '__main__':
    main()
