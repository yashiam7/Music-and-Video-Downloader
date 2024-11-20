import pytube
vid=[".avi",".mp4",".mkv",".mov"]
aud=[".wav",".mp3",".aac"]
def youtubedownload(url="",dir="file to be saved in directory"):
    while True:
        va=input("Enter Download Music or Video[aud/vid]:").lower()
        if url.startswith("https://www.youtube.com/") or url.startswith("https://www.youtube.com/watch?v="):
            yt=pytube.YouTube(url)
            print(f"Title:{yt.title}")
            if va=="vid":
                print("Video Resolutions:")
                for t in yt.streams.filter(progressive=True):
                    print(t.resolution(),end="||")
                r=input("Enter resolution:")
                print(vid,sep="||")
                fo=input("Enter format for video:")
                try:
                    if r:
                        yd=yt.streams.filter(progressive=True,resolution=r).first()
                    else:
                        yd=yt.streams.filter(progressive=True).order_by("resolution").desc().first()
                    print("Size",yd._filesize())
                    c=input("Continue Download[y/n]:")
                    if c.lower()=="y":
                        yd.download(dir,filename=yt.title+fo)
                        break
                except (pytube.exceptions.RegexMatchError, AttributeError) as e:
                    print(f"Error getting resolution: {e}")
                    continue  # Retry download loop
                except pytube.exceptions.PytubeError as e:
                    print(f"Rate limit exceeded: {e}")
                    break
            elif va=="aud":
                print("Audio formats:")
                print(aud,sep="||")
                fo=input("Enter format for audio:")
                yd=yt.streams.filter(only_audio=True).first()
                print("Size",yd._filesize())
                c=input("Continue Download[y/n]:")
                if c.lower()=="y":
                    yd.download(dir,filename=yt.title+fo)
                    break
            else:
                print("Invalid!!!")
                break
        else:
            req=pytube.Search().list(part="snippet",query=url,maxResults=15)
            res=req.execute()
        for i in range(len(res["items"])):
            print(f"{i+1}=>\nTitle: {i['snippet']['title']}")
            print(f"Channel:{i['snippet']["channelTitle"]}")
            print(f"Video ID: {i['id']['videoId']}")
        try:
            x=input("Video no:")
            url1=f"https://www.youtube.com/watch?v={res["items"][i-1]['id']['videoId']}"
            youtubedownload(url1,dir)
            break
        except (ValueError,IndexError):
            print("Invalid video no:try again")
            continue
