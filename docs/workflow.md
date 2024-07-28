## Using Workflow

### Fetch Playlist

(make sure playlist is public)

```
sh ./src/download_youtube_playlist.py 'https://www.youtube.com/playlist?list=PL1ksgbct81C50N23-IsrzlUVGJBBvZgbL'
```

it will create a file *./data/playlist_july24-podcast.txt* listing video ids

### Process Playlist

```
sh ./src/process_all.sh ./data/playlist_july24-podcast.txt 1 96 --temperature 0.1
```

it will start processing all the videos in playlist to produce $id-hashnode.md for each file

important reason of running shell script behind actual "bun video_to_hashnode.ts" that it will open markdown output for review before processing to the next one, and it will opened in helix editor in same terminal tab

### Configure CLI Tabs (optional)

Generate configuration:

```
sh ./src/generate_tabs.sh 96 3
```

it will create file config.txt

```
2-to-32: sh ./src/process_all.sh ./data/playlist_july24-podcast.txt 2 32 --temperature 0.1
33-to-64: sh ./src/process_all.sh ./data/playlist_july24-podcast.txt 33 64 --temperature 0.5
65-to-96: sh ./src/process_all.sh ./data/playlist_july24-podcast.txt 65 96 --temperature 0.9
```

run "sh ./scripts/open_tabs.sh" from GurrAI package

it will start processing three videos in parallel in separate tabs
