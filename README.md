# YouTubePlaylistCreator

## Setup

1. Create a youtube channel by logging into your google account on youtube:
![youtube_signup_picture](static/Screenshot%202026-01-28%20at%2020.24.46.png)
2. Create a Youtube channel by clicking on your profile picture and selecting 'create channel'
3. Go to https://console.cloud.google.com/
4. Sign in with the **Google account that owns your YouTube channel.**
5. Create or select a project by going to: **Project Selector -> New Project**
![top bar](static/top_bar.png)
![new_project](static/new_project.png)
6. Click **Create**
7. Enable the **YouTube Data API**

    - Left sidebar -> **API & Services** 
    - Click **Library**
![button](static/sidebar_button.png)
![sidebar](static/sidebar.png)
    - Search for **YouTube Data API v3**
    - Press **Enable**
![dataapi](static/youtube_data.png)

8. Configure OAuth consent screen

    - **APIs & Services -> OAuth consent screen**
![oauth-consent](static/Oauth_consent.png)
    - User Type: External (unless you're in a Google Workspace org)
    - click **Create**
9. Fill in the minimum required fields:

    - **App name**: anything (eg _YouTube Playlist Builder_)
    - **User support email**
    - **Developer contact email**

10. Click **Save and Continue** until done
11. Create OAuth credentials(Desktop App)

    - **APIs & Services -> Credentials**
    - Click **+ Create Credentials**
    - Choose **OAuth client ID**
![credentials](static/credentials.png)
    - Application type: **Desktop app**
    - Name it (anything)
    - Click **Create**
12. Download the file and rename to `client_secret.json`
13. Put this file within your project directory.

## Source

https://musicchartsarchive.com
![music_charts](static/music_charts.png)

When inputting the date, be sure to choose from one of the dates above!
Some days will not work (at the moment)