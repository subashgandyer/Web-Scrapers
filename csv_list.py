import csv
# with open('cuisine_2000_dishes.csv', 'rb') as input:
#      print zip(csv.reader(input, delimiter = ','))
    
#      dishes_list = []
#      reader = csv.reader(input, delimiter = ',')
#      dishes_list.append(reader)
   
# print dishes_list


# import csv
with open('cuisine_2000_dishes.csv', 'rb') as f:
    reader = csv.reader(f)
    #print reader
    your_list = list(reader)

print your_list