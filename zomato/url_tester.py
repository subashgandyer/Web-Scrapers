from urls import urls

b = []

for url in urls:
	print url[0]
	print url[0] + '/reviews'
	b.append(url[0]+'/reviews')


print b