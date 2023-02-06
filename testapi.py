import requests, random,time
import matplotlib.pyplot as plt

# policy indicates %of write
policy = 0.8
# max number of iteration
MaxNum = 30
url = "http://3.133.126.14:5000/api/"

read_url = url + "key/"
write_url = url + "upload"
imgs = {1: "1.jpg", 2: "2.jpg", 3: "3.jpg", 4: "4.png", 5: "5.gif", 6: "6.gif", 7: "7.jpg", 8: "8.jpg"}

# first put all images into db
for x in range(8):
    multipart_form_data = {
        'file': open(imgs[x + 1], "rb")
    }
    r = requests.post(write_url, data={'key': str(x + 1)}, files=multipart_form_data)

"""
latency_array=[]
for Num in range(1,MaxNum+1,4):
    RandomList = [random.random() for iter in range(Num)]
    latency = 0
    for x in RandomList:
        img_id = random.randint(1, 8)
        if x <= policy:
            multipart_form_data = {
                'file': open(imgs[img_id], "rb")
            }
            latency += requests.post(write_url, data={'key': str(img_id)},
                                     files=multipart_form_data).elapsed.total_seconds()
        else:
            latency += requests.post(read_url + str(img_id)).elapsed.total_seconds()
    latency_array.append(latency/Num)

print(latency_array)
plt.plot(range(1,MaxNum+1,4),latency_array)
plt.show()
requests.post(url+"delete_all")
"""
tputarray=[]

for a in range(10):
    t_record=time.time()+1
    tput=0
    while time.time() < t_record:
        x=random.random()
        img_id = random.randint(1, 8)
        if x <= policy:
            multipart_form_data = {
                'file': open(imgs[img_id], "rb")
            }
            requests.post(write_url, data={'key': str(img_id)},
                                         files=multipart_form_data)
        else:
            requests.post(read_url + str(img_id))
        tput+=1
    tputarray.append(tput)


for a in range(10):
    if a!=0:
        tputarray[a]=tputarray[a]+tputarray[a-1]
print(tputarray)
plt.plot(range(1,11),tputarray)
plt.show()
requests.post(url+"delete_all")