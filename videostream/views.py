from django.shortcuts import render,redirect
from .models import video
import youtube_dl
import json
from django.http import HttpResponse 


def index(request):
	vid = video.objects.all()
	return render(request,'index.html',{'vid': vid,})


def downloader(request):
	if request.method == 'POST':
		url = request.POST['url']
		ydl_opts = {}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			meta = ydl.extract_info(url,download=False)
		video_audio_stream = []
		for item in meta['formats']:
			file_size = item['filesize']
			if file_size is not None:
				file_size = f'{round(int(file_size)/1000000,2)}'
				resolution = 'audio'
			if item['height'] is not None:
				resolution = f"{item['height']} x {item['width']}"
			video_audio_stream.append({
            	'resolution' : resolution,
            	'filesize': file_size,
            	'url': item['url'],
            	'fps': item['fps'],
            	'extention':item['ext']
				})
			context = {
            'title': meta['title'], 'streams': video_audio_stream,
            'description': meta['description'], 'likes': meta['like_count'],
            'dislikes': meta['dislike_count'], 'thumb': meta['thumbnails'][3]['url'],
            'duration': round(int(meta['duration'])/60, 2), 'views': f'{int(meta["view_count"]):,}','true':True
        }

		a = json.dumps(context)



		return HttpResponse(a)
	return render(request,'downloader.html',{})



		# try:
		# 	print("_________in try+-----________")
		# 	url = request.POST['url']
		# 	tag = request.POST['itag']
		# 	print("the value of tag",tag)
		# 	print(url)
		# 	yt = YouTube(url)
		# 	ys = yt.streams.get_by_itag(tag)
		# 	ys.download()
		# 	response = FileResponse(open('download.jpg', 'rb'))
		# 	return response
		# except Exception as e:
		# 	print("_________in Exception+-----________",e)
		# 	url = request.POST['url']
		# 	yt = YouTube(url)
		# 	#Title of video
		# 	print("Title: ",yt.title)
		# 	#Number of views of video
		# 	print("Number of views: ",yt.views)
		# 	#Length of the video
		# 	print("Length of video: ",yt.length,"seconds")
		# 	#Description of video
		# 	print("Ratings: ",yt.rating)
		# 	stream = yt.streams.all()
		# 	config = []
		# 	for x in stream:
		# 		config.append([x.itag,x.resolution,x.fps])
		# 	return render(request,'downloader.html',{'title':yt.title,'views':yt.views,'length':yt.length,'rating':yt.rating,'image':yt.thumbnail_url,'true':True,'stream':config,'vdourl':url})
	return render(request,'downloader.html',{'item':item})
