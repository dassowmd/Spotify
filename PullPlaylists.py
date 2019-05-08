import sys
import spotipy
import spotipy.util as util
import pandas

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print "   %d %s %s" % (i, track['artists'][0]['name'],
            track['name'])

def checkDups(dataframe):
    print dataframe


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = raw_input('What is your user name?')
        # print "Whoops, need your username!"
        # print "usage: python user_playlists.py [username]"
        # sys.exit()

    token = util.prompt_for_user_token(username, client_id = 'a5810083e9c14fb6a60301f71cb325da',
        client_secret = '2a0486847eb047a0acddda104d28a783', redirect_uri = 'https://facebook.com/',
                                       scope='playlist-modify-private playlist-modify-public user-library-modify')

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        plTemp = pandas.DataFrame()
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print
                print playlist['name']
                print '  total tracks', playlist['tracks']['total']
                results = sp.user_playlist(username, playlist['id'],
                                           fields="tracks,artists,next")
                # artists=results[]
                tracks = results['tracks']
                while len(plTemp) < tracks['total']:
                    for key, track in enumerate(tracks['items']):
                        trackTemp = {'id': track['track']['id'], 'artist': track['track']['artists'],
                                     'track': track['track']['name'], 'playlist': playlist}
                        plTemp = plTemp.append(trackTemp, ignore_index=True)
                        # show_tracks(tracks)
                    if tracks['next']:
                        tracks = sp.next(tracks)
                show_tracks(tracks)
            # checkDups(plTemp)
    else:
        print "Can't get token for", username